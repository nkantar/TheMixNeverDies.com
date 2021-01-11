#!/usr/bin/env python3


from collections import defaultdict
import json
import shutil

from dateutil import parser, tz
import spotipy

from constants import (
    ARCHIVE_DIR_PATH,
    ARCHIVE_PATH,
    ARCHIVE_TEMPLATE_NAME,
    HOMEPAGE_DATES,
    HOMEPAGE_PATH,
    HOMEPAGE_TEMPLATE_NAME,
    INPUT_FILE_PATH,
    INPUT_TEMPLATE_PATH,
    OUTPUT_DIR_PATH,
    OUTPUT_STATIC_DIR_PATH,
    PAGE_TEMPLATE_NAME,
    SPOTIFY_ACCESS_TOKEN,
    SPOTIFY_CACHE_PATH,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_REFRESH_TOKEN,
    SPOTIFY_SCOPE,
    SPOTIFY_USERNAME,
    STATIC_DIR_PATH,
)
from helpers import populate_template, write_file


def generate_cache_file():
    cache = {
        "access_token": SPOTIFY_ACCESS_TOKEN,
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
        "scope": "user-library-read",
        "expires_at": 0,
    }
    contents = json.dumps(cache)
    write_file(SPOTIFY_CACHE_PATH, contents=contents)


def auth():
    oauth = spotipy.oauth2.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        cache_path=SPOTIFY_CACHE_PATH,
        username=SPOTIFY_USERNAME,
        open_browser=False,
    )
    oauth.refresh_access_token(SPOTIFY_REFRESH_TOKEN)
    sp = spotipy.Spotify(auth_manager=oauth)

    return sp


def _track_date(dt_str):
    dt = parser.parse(dt_str)
    dt_utc = dt.replace(tzinfo=tz.gettz("UTC"))
    dt_pacific = dt_utc.astimezone(tz.gettz("America/Los_Angeles"))

    dt_pacific_str = dt_pacific.isoformat()[:10]

    return dt_pacific_str


def fetch_tracks(sp):
    page = {"next": True}
    tracks = []
    offset = 0
    while page["next"]:
        page = sp.current_user_saved_tracks(limit=20, offset=offset)
        tracks.extend(
            [
                {"date": _track_date(track["added_at"]), "id": track["track"]["id"]}
                for track in page["items"]
            ]
        )

        offset += 20

    return tracks


def _ensure_dir(path):
    path.mkdir()


def clean_output():
    # create fresh output/ dir
    try:
        shutil.rmtree(OUTPUT_DIR_PATH)
    except FileNotFoundError:
        pass
    finally:
        _ensure_dir(OUTPUT_DIR_PATH)


def _older_post_date(dates, date):
    date_idx = dates.index(date)

    # oldest post has no older
    if date_idx == (len(dates) - 1):
        return

    older_idx = date_idx + 1
    older_date = dates[older_idx]
    return older_date


def _newer_post_date(dates, date):
    date_idx = dates.index(date)

    # newest post has no newer
    if date_idx == 0:
        return

    newer_idx = date_idx - 1
    newer_date = dates[newer_idx]
    return newer_date


def generate_posts(tracks):
    posts_dict = defaultdict(list)
    for track in tracks:
        posts_dict[track["date"]].append(track["id"])

    dates = sorted(posts_dict.keys(), reverse=True)

    posts = [
        {
            "date": date,
            "tracks": posts_dict[date],
            "newer": _newer_post_date(dates, date),
            "older": _older_post_date(dates, date),
        }
        for date in dates
    ]

    return posts


def generate_homepage(posts):
    contents = populate_template(
        HOMEPAGE_TEMPLATE_NAME, data={"posts": posts[:HOMEPAGE_DATES]}
    )
    write_file(HOMEPAGE_PATH, contents=contents)


def generate_archive(posts):
    _ensure_dir(ARCHIVE_DIR_PATH)
    contents = populate_template(
        ARCHIVE_TEMPLATE_NAME, data={"page_title": "Archive", "posts": posts}
    )
    write_file(ARCHIVE_PATH, contents=contents)


def generate_pages(posts):
    for post in posts:
        post_dir_path = ARCHIVE_DIR_PATH / post["date"]
        _ensure_dir(post_dir_path)

        post_page_path = post_dir_path / "index.html"
        contents = populate_template(
            PAGE_TEMPLATE_NAME,
            data={"page_title": f"Archive: {post['date']}", "post": post},
        )
        write_file(post_page_path, contents=contents)


def copy_static():
    shutil.copytree(STATIC_DIR_PATH, OUTPUT_STATIC_DIR_PATH)


def spotify():
    # generate cache file
    generate_cache_file()

    # auth
    sp = auth()

    # get playlist data
    tracks = fetch_tracks(sp)

    # format tracks into posts
    posts = generate_posts(tracks)

    # clean output/
    clean_output()

    # generate homepage
    generate_homepage(posts)

    # generate archive
    generate_archive(posts)

    # generate pages
    generate_pages(posts)

    # copy static
    copy_static()


if __name__ == "__main__":
    spotify()
