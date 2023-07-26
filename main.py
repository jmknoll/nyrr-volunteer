from nyrr import NYRRInterface
from mailer import Mailer


def main():
    nyrr = NYRRInterface()
    mailer = Mailer()

    results = nyrr.find_opportunities()
    print(results)


main()
