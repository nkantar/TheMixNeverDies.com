import django_rq
from tmnd.core.logger import log

from tmnd.cms.models import Member


def create_member(user, sociallogin, **kwargs):
    log.info(f"Creating member for user: {sociallogin}")

    member = Member(
        user=user,
        spotify_refresh_token=sociallogin.token.token_secret,
        member_spotify_id=sociallogin.account.uid,
    )
    member.save()

    log.info(f"Member created: {member.member_spotify_id}")

    member.create_playlist()

    member.update_playlist()


def enqueue_create_member(user, sociallogin, **kwargs):
    django_rq.enqueue(create_member, user, sociallogin)
