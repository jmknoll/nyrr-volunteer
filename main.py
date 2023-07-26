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

# save remaining to send email

# alert for an unexpected results
# rate-limit
# IP blocked


limit = 8
offset = 0
total_loaded = 8
last_page = False

available_runs = []
total_runs = 0
descriptions = []

while not last_page:
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
