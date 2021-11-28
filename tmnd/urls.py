from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("", include("tmnd.cms.urls")),
    path("", include("tmnd.main.urls")),
    path("django-rq/", include("django_rq.urls")),
]
