from loguru import logger

from django.core.management.base import BaseCommand

from tmnd.cms.models import Member


class Command(BaseCommand):
    help = "Update specific user's playlist"

    def add_arguments(self, parser):
        parser.add_argument("username", nargs=None, type=str)

    def handle(self, *args, username, **kwargs):
        logger.info(f"Updating playlist for user: {username}")

        user = Member.objects.get(member_spotify_id=username)

        try:
            user.create_playlist()
        except ValueError:
            pass

        user.update_playlist()
