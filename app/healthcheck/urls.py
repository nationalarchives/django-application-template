from django.conf import settings
from django.http import HttpResponse
from django.urls import path


def healthcheck(request):
    return HttpResponse("ok")


def healthcheck_version(request):
    return HttpResponse(settings.BUILD_VERSION)


app_name = "healthcheck"
urlpatterns = [
    path(
        "live/",
        healthcheck,
    ),
    path(
        "version/",
        healthcheck_version,
    ),
]
