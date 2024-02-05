from email import policy, message_from_bytes
from email.message import EmailMessage
from aiosmtpd.controller import UnthreadedController
from aiosmtpd.smtp import log as mail_log
import asyncio
import requests
import logging
import conf
from typing import List


class MailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return "250 OK"

    async def handle_DATA(self, server, session, envelope):
        logging.info(f"Message: '{envelope.mail_from}' -> '{envelope.rcpt_tos}'")

        msg = message_from_bytes(envelope.content, policy=policy.default)
        success = self._handle_message(envelope.rcpt_tos, msg)

        if not success:
            return "554 Message couldnt be handled"
        return "250 Message accepted for delivery"

    def _handle_message(self, recipients: List[str], msg: EmailMessage):
        found_attachment = False
        for a in msg.iter_attachments():
            found_attachment = True

            for r in recipients:
                if r not in conf.recipients:
                    logging.error(
                        f"Received mail for recipient '{r}', but not configured"
                    )
                    return False
                recipient = conf.recipients[r]

                logging.info(f"Uploading attachment '{a.get_filename()}' for '{r}'")

                res = requests.post(
                    recipient["PaperlessApiEndpoint"],
                    headers={"Authorization": f"Token {recipient['PaperlessToken']}"},
                    files={
                        "document": (
                            a.get_filename(),
                            a.get_content(),
                            "application/pdf",
                        )
                    },
                )
                if res.status_code != 200:
                    logging.error(
                        f"Upload to paperless failed with code {res.status_code}: {res.text}"
                    )
                    return False

        return found_attachment


def main():
    # set main log level to info
    # SMTP server module should only log warnings
    logging.basicConfig(
        level=logging.INFO, format="[%(asctime)s %(levelname)s] %(message)s"
    )
    mail_log.setLevel(logging.WARNING)

    # asyncio setup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # start the SMTP server
    logging.info("Starting SMTP server")
    controller = UnthreadedController(
        MailHandler(), hostname=conf.smtp_bind_host, port=conf.smtp_port, loop=loop
    )
    controller.begin()
    logging.info(
        f"SMTP listening on host '{controller.hostname}' port {controller.port}"
    )
    loop.run_forever()


if __name__ == "__main__":
    main()
