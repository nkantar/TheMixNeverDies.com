from django.urls import path

from tmnd.main.views import (
    HomeView,
    LoginRedirectView,
    LogoutRedirectView,
    UserRedirectView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("user/", UserRedirectView.as_view(), name="user-redirect"),
    path("login/", LoginRedirectView.as_view(), name="main-login-redirect"),
    path("logout/", LogoutRedirectView.as_view(), name="main-logout-redirect"),
]
