#!/usr/bin/env python3


from collections import defaultdict
from pathlib import Path
from shutil import copy, rmtree
from string import Template


SPLIT_CHAR = "|"
INDEX_DATES = 7

CURRENT_DIR_PATH = Path.cwd()
INPUT_FILE_PATH = CURRENT_DIR_PATH / "input"
OUTPUT_DIR_PATH = CURRENT_DIR_PATH / "output"
OUTPUT_FILE_PATH = OUTPUT_DIR_PATH / "index.html"
TEMPLATE_FILE_PATH = CURRENT_DIR_PATH / "template.html"

ASSET_FILE_NAMES = ["normalize.css", "style.css"]


POST_HTML = Template("<h2>$date</h2>$embeds_html\n")
EMBED_HTML = Template(
    "<iframe src='https://open.spotify.com/embed/track/$track_id' "
    "width='300' height='380' frameborder='0' allowtransparency='true' "
    "allow='encrypted-media'></iframe>"
)


def _ensure_track_id(track_id):
    # https://open.spotify.com/track/7kPLrLCWRoevQlUY80I0nC?si=S7ieVaOoR7KcfiY_d8f1IA

    # if URL, extract track ID
    if track_id.startswith("https://"):
        return track_id.split("/")[-1].split("?")[0]

    # if not URL, assume track ID
    return track_id


def _posts_by_date(raw_lines):
    posts = defaultdict(str)

    for line in raw_lines:
        date, track_id = line.split(SPLIT_CHAR)
        track_id = _ensure_track_id(track_id)

        embed_html = EMBED_HTML.substitute(track_id=track_id)

        # reverse track order within each post
        posts[date] = embed_html + posts[date]

    return posts


def generate_index():
    with open(INPUT_FILE_PATH) as input_file:
        raw_lines = input_file.read().splitlines()

        posts = _posts_by_date(raw_lines)

        html = "".join(
            [
                POST_HTML.substitute(date=date, embeds_html=posts[date])
                for date in list(reversed(list(posts.keys())))[:INDEX_DATES]
            ]
        )

        try:
            rmtree(OUTPUT_DIR_PATH)
        except FileNotFoundError:
            pass

        OUTPUT_DIR_PATH.mkdir()

        with open(TEMPLATE_FILE_PATH) as template_file:
            output_template = Template(template_file.read())
            output = output_template.substitute(content=html)

            with open(OUTPUT_FILE_PATH, "w") as output_file:
                output_file.write(output)


def copy_assets():
    for asset_file_name in ASSET_FILE_NAMES:
        copy(CURRENT_DIR_PATH / asset_file_name, OUTPUT_DIR_PATH / asset_file_name)


def build():
    generate_index()
    copy_assets()


if __name__ == "__main__":
    build()
