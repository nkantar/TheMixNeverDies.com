from collections import defaultdict
from datetime import date, timedelta

from loguru import logger

from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.views.generic import RedirectView, TemplateView, View

from tmnd.cms.models import Track


class AbstractUserView(View):
    @property
    def username(self):
        username, *unused = self.request.get_host().split(".")
        return username


class UserHomeView(AbstractUserView, TemplateView):
    template_name = "track_list.html"

    def get_context_data(self):
        datetimes = (
            Track.objects.filter(member__member_spotify_id=self.username)
            .order_by("-added")
            .values_list("added", flat=True)
        )
        dates = sorted(
            list(set([datetime_.date() for datetime_ in datetimes])),
            reverse=True,
        )[: settings.PAGE_SIZE]

        tracks = Track.objects.filter(
            member__member_spotify_id=self.username,
            added__date__gte=dates[-1],
            added__date__lte=dates[0],
        ).order_by("-added")

        tracks_per_date = defaultdict(list)
        for track in tracks:
            tracks_per_date[track.added.date()].append(track)

        context_data = {
            "dates": [
                {
                    "date_": date_,
                    "tracks": tracks_per_date[date_],
                }
                for date_ in dates
            ]
        }
        return context_data


class UserDateView(AbstractUserView, TemplateView):
    template_name = "track_list.html"

    def get_context_data(self, **kwargs):
        date_ = date.fromisoformat(self.kwargs["date"])

        tracks = Track.objects.filter(
            member__member_spotify_id=self.username,
            added__date=date_,
        ).order_by("-added")

        context_data = {"dates": [{"date_": date_, "tracks": tracks}]}
        return context_data


class UserArchiveView(AbstractUserView, TemplateView):
    template_name = "archive.html"

    def get_context_data(self, **kwargs):

        dates = (
            Track.objects.annotate(added_date=TruncDate("added"))
            .filter(member__member_spotify_id=self.username)
            .values("added_date")
            .annotate(track_count=Count("id"))
            .values("added_date", "track_count")
            .order_by("-added_date")
        )

        # dates = (
        #     Track.objects.filter(member__member_spotify_id=self.username)
        #     .order_by("-added")
        #     .values("added")
        # ).annotate(track_count=Count("id"))
        context_data = {"dates": dates}
        return context_data


class UserLoginRedirectView(RedirectView):
    url = settings.LOGIN_PATH


class UserLogoutRedirectView(RedirectView):
    url = settings.LOGOUT_PATH
