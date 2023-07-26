import requests
from bs4 import BeautifulSoup


class NYRRInterface:
    def __init__(self):
        # init config
        self.limit = 8
        self.offset = 0
        self.total_loaded = 8
        self.last_page = False

        self.headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }

        self.url = "https://www.nyrr.org/api/feature/volunteer/FilterVolunteerOpportunities?available_only=true&itemId=3EB6F0CC-0D76-4BAF-A894-E2AB244CEB44&limit={limit}&offset={offset}&totalItemLoaded={total_loaded}"

    def find_opportunities(self):
        available_runs = []
        total_runs = 0
        descriptions = []

        while not self.last_page:
            res = requests.get(self.url, headers=self.headers)
            # probably check for errors here
            print(f"Response status code: {res.status_code}")
            print(f"Response headers: {res.headers}")
            return

            data = res.json()

            if data["lastPage"] == True:
                self.last_page = True
            html = data["html"]
            soup = BeautifulSoup(html, "html.parser")
            opps = soup.find_all("section", class_="role_listing")
            for opp in opps:
                total_runs += 1
                avail = self.is_available(opp)
                if avail:
                    available_runs.append(opp)
            self.offset += 8

        if len(available_runs) > 0:
            for opp in available_runs:
                descriptions.append(self.extract_title(opp))
            return descriptions
            # send email or text with options
        else:
            return f"No available runs at this time. Total runs: {total_runs}"

    # extract role title and event from volunteer opportunity
    def extract_title(self, opp):
        title = opp.select_one(".role_listing__title")
        event = opp.select_one(".role_listing__event")
        hr_title = title.contents[0].strip()
        hr_event = event.contents[0].strip()
        return (hr_title, hr_event)

    # infer avialability and relevance of opportunity
    def is_available(opp):
        # is a medical volunteer opportunity
        med = opp.select_one(".medical_icon")
        if med is not None:
            return False
        # is not a 9+1 opportunity
        free_run = opp.select_one(".tag.tag--no")
        if free_run is not None:
            return False
        else:
            return True
