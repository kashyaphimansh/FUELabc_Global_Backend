from .base import *
from decouple import config, Csv

DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=Csv()
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="",
    cast=Csv()
)

STATIC_ROOT = config(
    "STATIC_ROOT",
    default="/var/www/fuelabc_au_backend/shared/staticfiles"
)

MEDIA_ROOT = config(
    "MEDIA_ROOT",
    default="/var/www/fuelabc_au_backend/shared/media"
)

MEDIA_URL = "/media/"

# Required because Nginx will proxy requests to Gunicorn.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# RDS PostgreSQL SSL mode. In production this should be require.
DATABASES["default"]["OPTIONS"] = {
    "sslmode": config("DB_SSLMODE", default="require")
}

# Production CORS control.
CORS_ALLOW_ALL_ORIGINS = config(
    "CORS_ALLOW_ALL_ORIGINS",
    default=False,
    cast=bool
)

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="",
    cast=Csv()
)

# Cookie/security settings. Keep SSL redirect configurable because first deployment may be tested on IP/HTTP before domain SSL.
SESSION_COOKIE_SECURE = config(
    "SESSION_COOKIE_SECURE",
    default=True,
    cast=bool
)

CSRF_COOKIE_SECURE = config(
    "CSRF_COOKIE_SECURE",
    default=True,
    cast=bool
)

SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default=False,
    cast=bool
)

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "same-origin"

# HSTS should remain disabled until HTTPS/domain is fully confirmed.
SECURE_HSTS_SECONDS = config(
    "SECURE_HSTS_SECONDS",
    default=0,
    cast=int
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
    cast=bool
)

SECURE_HSTS_PRELOAD = config(
    "SECURE_HSTS_PRELOAD",
    default=False,
    cast=bool
)
