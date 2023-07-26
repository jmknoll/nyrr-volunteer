class Nyrr:
    def __init__(self, config):
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
      
      self.url =  "https://www.nyrr.org/api/feature/volunteer/FilterVolunteerOpportunities?available_only=true&itemId=3EB6F0CC-0D76-4BAF-A894-E2AB244CEB44&limit={limit}&offset={offset}&totalItemLoaded={total_loaded}"
        pass

    def find_opportunities(self):
        pass
      
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
