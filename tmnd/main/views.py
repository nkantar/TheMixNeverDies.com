from django.conf import settings
from django.views.generic import RedirectView, TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class UserRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        scheme = self.request.scheme
        host = self.request.get_host()
        username = self.request.user.username
        url = f"{scheme}://{username}.{host}"
        return url


class LoginRedirectView(RedirectView):
    url = settings.LOGIN_PATH


class LogoutRedirectView(RedirectView):
    url = settings.LOGOUT_PATH
