from django.urls import path

from tmnd.cms.views import (
    UserArchiveView,
    UserDateView,
    UserHomeView,
    UserLoginRedirectView,
    UserLogoutRedirectView,
)


# /archive/
# /playlist/


urlpatterns = [
    path("", UserHomeView.as_view(), name="user-home"),
    path("archive/", UserArchiveView.as_view(), name="user-archive"),
    path("archive/<str:date>/", UserDateView.as_view(), name="user-date"),
    path("login/", UserLoginRedirectView.as_view(), name="user-login-redirect"),
    path("logout/", UserLogoutRedirectView.as_view(), name="user-logout-redirect"),
]
