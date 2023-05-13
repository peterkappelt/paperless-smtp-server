from os import environ
import urllib.parse

PAPERLESS_HOST = urllib.parse.urlparse(environ["PAPERLESS_HOST"]).geturl()
PAPERLESS_TOKEN = environ["PAPERLESS_TOKEN"]

SMTP_BIND_HOST = environ.get("SMTP_BIND_HOST", "")
SMTP_PORT = environ.get("SMTP_PORT", 8025)
