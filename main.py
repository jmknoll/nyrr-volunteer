from nyrr import NYRRInterface
from mailer import Mailer

from util import Status
from config import FROM_EMAIL, TO_EMAIL, MESSAGE_STREAM


def main():
    nyrr = NYRRInterface()
    mailer = Mailer()

    results = nyrr.find_opportunities()

    if results["status"] == Status.SUCCESS:
        print(results["message"])

        from_email = FROM_EMAIL
        to_email = TO_EMAIL
        subject = "[Automated] - NYRR Volunteer Opportunities"
        body = format_list_as_html(results)
        stream = MESSAGE_STREAM
        # from, to, subject, body, stream
        mail_response = mailer.send(from_email, to_email, subject, body, stream)
        if mail_response["ErrorCode"] == 0:
            print("mail success")
        else:
            print(f'mail error: {mail_response["Message"]}')

    # handle no results or error
    else:
        print(results["message"])


def format_list_as_html(opps):
    list_items = [f"<li>{opp}</li>" for opp in opps]
    return f"<ul>{''.join(list_items)}</ul>"


main()
