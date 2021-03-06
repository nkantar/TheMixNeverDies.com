.DEFAULT_GOAL := help
.PHONY: help build devserve watch

help: ## this help dialog
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## build site in output/
	poetry run ./build.py

devserve: ## serve dev version of site
	poetry run python3 -m http.server 8000 -d output/

watch: ## watch for rebuilt and regen custom and css
	modd

netlify: ## build an deploy site on netlify
	pip install spotipy jinja2 python-dotenv python-dateutil && ./build.py
