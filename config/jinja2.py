import json
import os
import tomllib

from django import template
from django.conf import settings
from django.templatetags.static import StaticNode
from django.urls import reverse
from django.utils.safestring import mark_safe
from jinja2 import Environment

from app.lib.context_processor import now_iso_8601
from app.lib.template_filters import slugify

register = template.Library()


class StaticNodeWithVersion(StaticNode):
    @classmethod
    def handle_simple(cls, path, **kwargs):
        url = super().handle_simple(path)
        if kwargs:
            url += "?" + "&".join(
                [f"{parameter}={kwargs[parameter]}" for parameter in kwargs]
            )
        return mark_safe(url)


@register.tag("static")
def do_static_with_version(parser, token):
    return StaticNodeWithVersion.handle_token(parser, token)


def static_with_version(path, **kwargs):
    return StaticNodeWithVersion.handle_simple(path, **kwargs)


def environment(**options):
    env = Environment(**options)

    TNA_FRONTEND_VERSION = ""
    try:
        package_lock_json_path = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "../",
            "package-lock.json",
        )
        with open(package_lock_json_path, "r") as package_lock_json:
            data = json.load(package_lock_json)
            TNA_FRONTEND_VERSION = (
                data.get("packages", {})
                .get("node_modules/@nationalarchives/frontend", {})
                .get("version", "")
            )
    except FileNotFoundError:
        # Error getting version of TNA frontend
        pass

    TNA_FRONTEND_JINJA_VERSION = ""
    try:
        poetry_lock_toml_path = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "../",
            "poetry.lock",
        )
        with open(poetry_lock_toml_path, "rb") as poetry_lock_toml:
            data = tomllib.load(poetry_lock_toml)
            for package in data.get("package", []):
                if package.get("name") == "tna-frontend-jinja":
                    TNA_FRONTEND_JINJA_VERSION = package.get("version", "")
                    break
    except FileNotFoundError:
        # Error getting version of TNA frontend Jinja
        pass

    env.globals.update(
        {
            "static": static_with_version,
            "app_config": {
                "ENVIRONMENT_NAME": settings.ENVIRONMENT_NAME,
                "GA4_ID": settings.GA4_ID,
                "CONTAINER_IMAGE": settings.CONTAINER_IMAGE,
                "BUILD_VERSION": settings.BUILD_VERSION,
                "TNA_FRONTEND_VERSION": TNA_FRONTEND_VERSION,
                "TNA_FRONTEND_JINJA_VERSION": TNA_FRONTEND_JINJA_VERSION,
                "COOKIE_DOMAIN": settings.COOKIE_DOMAIN,
                "COOKIE_PREFERENCES_URL": settings.COOKIE_PREFERENCES_URL,
            },
            "url_for": reverse,
            "now_iso_8601": now_iso_8601,
        }
    )
    env.filters.update({"slugify": slugify})
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.autoescape = True
    return env
