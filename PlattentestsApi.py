import requests
import constants

class PlattentestsApi:

    @staticmethod
    def getHighlightsFromLatestReview():
        response = requests.get(constants.plattentests_review_api_endpoint)
        reviews = response.json()
        trackHighlights = []
        for r in reviews:
            for th in r["trackHighlights"]:
                if th == "-":
                    continue
                trackHighlights.append(str(r["band"] + " - " + th))
        return trackHighlights
    
    @staticmethod
    def getAlbumOfTheWeek():
        response = requests.get(constants.plattentests_review_api_endpoint)
        reviews = response.json()
        for r in reviews:
            if r["albumOfTheWeek"] != "0000-00-00":
                return r["band"] + " - " + r["title"]
        raise Exception('No album of the week found')