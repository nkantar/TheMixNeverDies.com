from os import getenv

from dotenv import load_dotenv
from loguru import logger

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from allauth.socialaccount.models import SocialApp


load_dotenv()

SUPERUSER_USERNAME = getenv("SUPERUSER_USERNAME")
SUPERUSER_EMAIL = getenv("SUPERUSER_EMAIL")
SUPERUSER_PASSWORD = getenv("SUPERUSER_PASSWORD")


class Command(BaseCommand):
    help = "Bootstrap initial app data"

    def handle(self, *args, **kwargs):
        logger.info("Bootstrapping initial app data")

        # create superuser
        logger.info(f"Creating superuser {SUPERUSER_USERNAME}")
        User = get_user_model()
        User.objects.create_superuser(
            SUPERUSER_USERNAME,
            SUPERUSER_EMAIL,
            SUPERUSER_PASSWORD,
        )

        # update site data
        logger.info("Updating site data")
        site = Site.objects.first()
        site.domain = "tmnd.local"
        site.name = "the mix never dies"
        site.save()

        # add Spotify social app
        logger.info("Creating social app")
        app = SocialApp(
            provider="spotify",
            name="Spotify",
            client_id=settings.SPOTIFY_CLIENT_ID,
            secret=settings.SPOTIFY_CLIENT_SECRET,
        )
        app.save()
        app.sites.set([site])
        app.save()
