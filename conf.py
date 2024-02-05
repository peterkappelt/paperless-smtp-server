from configparser import ConfigParser
from os import environ
import urllib.parse

CONFFILE = environ.get("CONFFILE", "config.ini")

print(f"Reading config from '{CONFFILE}'")
conffile = ConfigParser()
conffile.read(CONFFILE)

smtp_bind_host = conffile.get("server", "BindHost", fallback="")
smtp_port = conffile.get("server", "Port", fallback=8025)

recipients = {}

for section in conffile.sections():
    if section == "server":
        continue

    recipients[section] = {
        "PaperlessHost": conffile.get(section, "PaperlessHost", fallback=None),
        "PaperlessToken": conffile.get(section, "PaperlessToken", fallback=None),
    }

    if (
        recipients[section]["PaperlessHost"] is None
        or recipients[section]["PaperlessToken"] is None
    ):
        raise ValueError(
            f"Recipient '{section}' is missing PaperlessHost or PaperlessToken"
        )

    recipients[section]["PaperlessApiEndpoint"] = urllib.parse.urljoin(
        recipients[section]["PaperlessHost"], "/api/documents/post_document/"
    )

if len(recipients) == 0:
    raise ValueError("No recipients specified in config.ini")
