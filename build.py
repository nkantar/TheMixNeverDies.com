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
    ERROR_404_PATH,
    ERROR_404_TEMPLATE_NAME,
    HOMEPAGE_DATES,
    HOMEPAGE_PATH,
    HOMEPAGE_TEMPLATE_NAME,
    OUTPUT_DIR_PATH,
    OUTPUT_STATIC_DIR_PATH,
    PAGE_TEMPLATE_NAME,
    PLAYLIST_DIR_PATH,
    PLAYLIST_PATH,
    PLAYLIST_TEMPLATE_NAME,
    SPOTIFY_ACCESS_TOKEN,
    SPOTIFY_CACHE_PATH,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_PLAYLIST_ID,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_REFRESH_TOKEN,
    SPOTIFY_SCOPE,
    SPOTIFY_USERNAME,
    STATIC_DIR_PATH,
)
from helpers import populate_template, write_file


def generate_cache_file():
    print("Generating cache file...")
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
    print("Authenticating...")
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
    print("Fetching tracks...")
    page = {"next": True}
    tracks = []
    offset = 0
    while page["next"]:
        print(f"Fetching tracks: offset {offset}...")
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
    print("Cleaning output dir...")
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
    print("Generating posts...")
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
    print("Generating homepage...")
    contents = populate_template(
        HOMEPAGE_TEMPLATE_NAME, data={"posts": posts[:HOMEPAGE_DATES]}
    )
    write_file(HOMEPAGE_PATH, contents=contents)


def generate_playlist_page(playlist_id):
    print("Generating playlist page...")
    _ensure_dir(PLAYLIST_DIR_PATH)
    contents = populate_template(
        PLAYLIST_TEMPLATE_NAME,
        data={
            "page_title": "Playlist",
            "playlist_id": playlist_id,
        },
    )
    write_file(PLAYLIST_PATH, contents=contents)


def clear_playlist(sp):
    print("Clearing playlist...")
    # fetch all playlist tracks
    page = sp.playlist_tracks(SPOTIFY_PLAYLIST_ID)
    offset = 0
    while page["items"]:
        print(f"Clearing playlist: offset {offset}...")
        page = sp.playlist_tracks(SPOTIFY_PLAYLIST_ID, offset=offset)
        sp.playlist_remove_all_occurrences_of_items(
            SPOTIFY_PLAYLIST_ID,
            items=[track["track"]["id"] for track in page["items"]],
        )

        offset += 100


def update_playlist(sp, tracks):
    print("Updating playlist...")
    pages = defaultdict(list)
    for idx, track in enumerate(tracks):
        page_idx = idx // 100
        pages[page_idx].append(track["id"])

    for page in reversed(list(pages.values())):
        sp.playlist_add_items(SPOTIFY_PLAYLIST_ID, page)


def generate_archive(posts):
    print("Generating archive...")
    _ensure_dir(ARCHIVE_DIR_PATH)
    contents = populate_template(
        ARCHIVE_TEMPLATE_NAME, data={"page_title": "Archive", "posts": posts}
    )
    write_file(ARCHIVE_PATH, contents=contents)


def generate_pages(posts):
    print("Generating pages...")
    for post in posts:
        print(f"Generating page: post {post['date']}...")
        post_dir_path = ARCHIVE_DIR_PATH / post["date"]
        _ensure_dir(post_dir_path)

        post_page_path = post_dir_path / "index.html"
        contents = populate_template(
            PAGE_TEMPLATE_NAME,
            data={"page_title": f"Archive: {post['date']}", "post": post},
        )
        write_file(post_page_path, contents=contents)


def generate_404():
    print("Generating 404...")
    contents = populate_template(ERROR_404_TEMPLATE_NAME)
    write_file(ERROR_404_PATH, contents=contents)


def copy_static():
    print("Copying static...")
    shutil.copytree(STATIC_DIR_PATH, OUTPUT_STATIC_DIR_PATH)


def spotify():
    print("Starting!")

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

    # generate playlist page
    generate_playlist_page(SPOTIFY_PLAYLIST_ID)

    # clear playlist
    clear_playlist(sp)

    # update playlist
    update_playlist(sp, tracks)

    # generate archive
    generate_archive(posts)

    # generate pages
    generate_pages(posts)

    # generate 404
    generate_404()

    # copy static
    copy_static()

    print("Finished!")


if __name__ == "__main__":
    spotify()
