from django.apps import AppConfig

from allauth.account.signals import user_signed_up


class CmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tmnd.cms"

    def ready(self):
        from tmnd.cms.signals import enqueue_create_member

        user_signed_up.connect(enqueue_create_member)
