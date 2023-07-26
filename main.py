from nyrr import NYRRInterface
from mailer import Mailer

from logger import Logger
from util import Status
from config import FROM_EMAIL, TO_EMAIL, MESSAGE_STREAM


def main():
    nyrr = NYRRInterface()
    mailer = Mailer()
    log = Logger().logger

    results = nyrr.find_opportunities()

    if results["status"] == Status.SUCCESS:
        log.info(results["message"])

        from_email = FROM_EMAIL
        to_email = TO_EMAIL
        subject = "[Automated] - NYRR Volunteer Opportunities"
        body = format_list_as_html(results["data"])
        stream = MESSAGE_STREAM
        # from, to, subject, body, stream
        mail_response = mailer.send(from_email, to_email, subject, body, stream)
        if mail_response["ErrorCode"] == 0:
            log.info("mail success")
        else:
            log.error(f'mail error: {mail_response["Message"]}')

    # handle no results or error
    else:
        log.error(results["message"])


def format_list_as_html(opps):
    list_items = [f"<li>{opp}</li>" for opp in opps]
    return f"<ul>{''.join(list_items)}</ul>"


main()
