import requests
import constants

class PlattentestsApi:
    def getHighlightsFromLatestReview(self):
        response = requests.get(constants.plattentests_api_endpoint)
        reviews = response.json()
        trackHighlights = ''
        for r in reviews:
            trackHighlights = trackHighlights + "\n".join(str(r["band"] + " - " + th) for th in r["trackHighlights"])
        return trackHighlights