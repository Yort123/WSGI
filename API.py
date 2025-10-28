import requests


class hockey:
    hockey_url = "https://api-web.nhle.com/v1/"
    def __init__(self):
        self.teamList = "0: Hurricanes, 1: Rangers"
        self.teams = ["WPG", "WSH", "VGK", "TOR", "DAL", "LAK", "TBL", "COL", "EDM", "CAR", "FLA", "OTT", "MIN", "STL",
                      "CGY", "NJD", "MTL", "VAN", "UTA", "CBJ", "DET", "NYR", "NYI", "PIT", "ANA", "BUF", "SEA", "BOS",
                      "PHI", "NSH", "CHI", "SJS"]
        self.pos = ["goalie", "forward", "defense"]
        self.playerId = []

    def playStats(self, id=None):
        urlPlayerStats = "https://api-web.nhle.com/v1/player/"
        landing = "/landing"
        urlPlayerStats = urlPlayerStats + str(id) + landing
        playerStats = requests.get(urlPlayerStats)
        playerStats = playerStats.json()
        return playerStats

    @staticmethod
    def getPlayers(team):
        pos = ["forwards", "defensemen", "goalies"]
        request_string = "https://api-web.nhle.com/v1/roster/" + team + "/current"
        test = requests.get(request_string)
        extract = test.json()
        playerInfo = []
        for i in pos:
            for n in extract[i]:
                """
                playerInfo gets first, last, id, team abbrev, position, only for current year (headshot and team logo)
                """
                playerInfo.append([n["firstName"]["default"], n["lastName"]["default"], n["id"], team,
                                   i, n["headshot"]])
        return playerInfo

    def get_team(self):
        test = requests.get("https://api-web.nhle.com/v1/standings/now")
        ex = test.json()
        return ex

    # def getStats(self, player=None):
    #     print("Player:", player)
    #     # player_info = db.getPlayer(player)
    #     # if player_info is not None:
    #     #     skater = [{"first": player_info[2], "last":player_info[3]}]
    #     for q in self.pos:
    #         for i in players[q]:
    #             stats = self.playStats(i["id"])
    #             stats = stats["featuredStats"]["regularSeason"]["subSeason"]
    #             if i["firstName"]["default"] == player:
    #                 stats = self.playStats(i["id"])
    #                 stats = stats["featuredStats"]["regularSeason"]["subSeason"]
    #                 skater = [{"first": i["firstName"]["default"], "last": i["lastName"]["default"], "stats": stats}]
    #                 return skater

    # def getNames(self, 1=0, year="20232024"):
    #
    #     players = "https://api-web.nhle.com/v1/roster/" + self.teams[team] + year
    #     names = []
    #     for n in self.pos:
    #         for i in players[n]:
    #             print(i)
    #             stats = self.playStats(i["id"])
    #             self.playerId += [{i["firstName"]["default"]: i["id"]}]
    #             if "featuredStats" in stats:
    #                 names += [{"first": i["firstName"]["default"], "last": i["lastName"]["default"]}]
    # return names

# test = Hockey()
# test.getPlayers()
# test.getNames(0)
