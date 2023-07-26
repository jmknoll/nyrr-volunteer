from nyrr import NYRRInterface
from mailer import Mailer

from util import Status


def main():
    nyrr = NYRRInterface()
    mailer = Mailer()

    results = nyrr.find_opportunities()
    if results.status == Status.SUCCESS:
      print(results.message)
    # handle no results or error
    else
    
    


main()
