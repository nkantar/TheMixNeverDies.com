# TheMixNeverDies.com

[**The Mix Never Dies**] (**TMND**) is a collection of songs in Nik’s Spotify “Liked
Songs” playlist.
As the tagline says, Nik likes these choonz.


## Overview

TMND is a static website generated from the content of my Spotify “Liked Songs”
playlist.

It’s got a homepage with the last 7 days of songs, and a daily archive.

The whole thing is generated using [Python], [Poetry], [spotipy], [Jinja],
[python-dotenv], [dateutil], and all their dependencies, and is deployed on [Netlify].
The deployment runs on every change to the `main` branch, and daily at 3:11AM Pacific
via [GitHub Actions].

Why 3:11AM? Because the `"11 11 * * *"` `cron` schedule syntax means I don’t have to
remember that the minute comes before the hour.


## Contributing

Unlike most of my projects, contributions are not explicitly encouraged, though they’re
not discouraged, either.

If there’s any real interest, I’d be open to turning this into something usable by
others.
However, I’m quite skeptical about that being the case, so…


## License

This project is released into the public domain via the [Unlicense].


[**The Mix Never Dies**]: https://themixneverdies.com/ "The Mix Never Dies"
[Python]: https://www.python.org/ "Welcome to Python.org"
[Poetry]: https://python-poetry.org/ "Poetry - Python dependency management and packaging made easy."
[spotipy]: https://github.com/plamere/spotipy "plamere/spotipy: A light weight Python library for the Spotify Web API"
[Jinja]: https://jinja.palletsprojects.com/en/2.11.x/ "Jinja — Jinja Documentation (2.11.x)"
[python-dotenv]: https://github.com/theskumar/python-dotenv "theskumar/python-dotenv: Get and set values in your .env file in local and production servers."
[dateutil]: https://dateutil.readthedocs.io/en/stable/ "dateutil - powerful extensions to datetime — dateutil 2.8.1 documentation"
[Netlify]: https://www.netlify.com/ "Netlify: Develop & deploy the best web experiences in record time"
[GitHub Actions]: https://github.com/actions "GitHub Actions"
[Unlicense]: https://unlicense.org/ "Unlicense.org » Unlicense Yourself: Set Your Code Free"
