import requests
from bs4 import BeautifulSoup

# main_url = "https://www.nyrr.org/getinvolved/volunteer/opportunities?available_only=true&itemId=3EB6F0CC-0D76-4BAF-A894-E2AB244CEB44&limit=8&offset=0&totalItemLoaded=8"


# spoof browser headers
headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

# Run against the target url until it returns true
# filter down the list to remove non 9+1 opportunities
# filter down the list to remove medical opportunities
# save remaining to send email

# alert for an unexpected results
# rate-limit
# IP blocked


# extract role title and event from volunteer opportunity
def extract_title(opp):
    title = opp.select_one(".role_listing__title")
    event = opp.select_one(".role_listing__event")
    hr_title = title.contents[0].strip()
    hr_event = event.contents[0].strip()
    return (hr_title, hr_event)


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


# save results to dynamo db


limit = 8
offset = 0
total_loaded = 8
last_page = False

available_runs = []
total_runs = 0
descriptions = []

while not last_page:
    url = f"https://www.nyrr.org/api/feature/volunteer/FilterVolunteerOpportunities?available_only=true&itemId=3EB6F0CC-0D76-4BAF-A894-E2AB244CEB44&limit={limit}&offset={offset}&totalItemLoaded={total_loaded}"
    res = requests.get(url, headers)
    # probably check for errors here
    data = res.json()
    if data["lastPage"] == True:
        last_page = True
    html = data["html"]
    soup = BeautifulSoup(html, "html.parser")
    opps = soup.find_all("section", class_="role_listing")
    for opp in opps:
        total_runs += 1
        avail = is_available(opp)
        if avail:
            available_runs.append(opp)
    offset += 8

if len(available_runs) > 0:
    for opp in available_runs:
        descriptions.append(extract_title(opp))
    print(descriptions)
    # send email or text with options
else:
    print(f"No available runs at this time. Total runs: {total_runs}")
