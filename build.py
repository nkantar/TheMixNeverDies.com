#!/usr/bin/env python3


from collections import defaultdict
import json
import shutil

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


def fetch_tracks(sp):
    page = {"next": True}
    tracks = []
    offset = 0
    while page["next"]:
        page = sp.current_user_saved_tracks(limit=20, offset=offset)
        tracks.extend(
            [
                {"date": track["added_at"][:10], "id": track["track"]["id"]}
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


def generate_posts(tracks):
    posts_dict = defaultdict(list)
    for track in tracks:
        posts_dict[track["date"]].append(track["id"])

    posts = [
        {"date": date, "tracks": posts_dict[date]}
        for date in sorted(posts_dict.keys(), reverse=True)
    ]

    return posts


def generate_homepage(posts):
    contents = populate_template(
        HOMEPAGE_TEMPLATE_NAME, data={"posts": posts[:HOMEPAGE_DATES]}
    )
    write_file(HOMEPAGE_PATH, contents=contents)


def generate_archive(posts):
    _ensure_dir(ARCHIVE_DIR_PATH)
    contents = populate_template(ARCHIVE_TEMPLATE_NAME, data={"posts": posts})
    write_file(ARCHIVE_PATH, contents=contents)


def generate_pages(posts):
    for post in posts:
        post_dir_path = ARCHIVE_DIR_PATH / post["date"]
        _ensure_dir(post_dir_path)

        post_page_path = post_dir_path / "index.html"
        contents = populate_template(PAGE_TEMPLATE_NAME, data={"post": post})
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
