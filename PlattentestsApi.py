import requests
import constants

class PlattentestsApi:

    @staticmethod
    def getHighlightsFromLatestReview():
        response = requests.get(constants.plattentests_review_api_endpoint)
        reviews = response.json()
        trackHighlights = []
        for r in reviews:
            trackHighlights.append([])
            for th in r["trackHighlights"]:
                if th == "-":
                    continue
                trackHighlights[-1].append(str(r["band"] + " - " + th))
        return trackHighlights
    
    @staticmethod
    def getAlbumOfTheWeek():
        response = requests.get(constants.plattentests_review_api_endpoint)
        reviews = response.json()
        for r in reviews:
            if r["albumOfTheWeek"] != "0000-00-00":
                return r["band"] + " - " + r["title"]
        raise Exception('No album of the week found')


    @staticmethod
    def getAlbumScoreValues():
        response = requests.get(constants.plattentests_review_api_endpoint)
        reviews = response.json()
        scoreValues = []
        for r in reviews:
            if r["albumOfTheWeek"] != "0000-00-00":
                scoreValues.append(11)
            elif r["value"] == "Ohne Bewertung":
                scoreValues.append(0)
            else:
                scoreValues.append(int(r["value"]))
        return scoreValues
