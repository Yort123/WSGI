import time
import requests
import datetime
current_year = str((datetime.date.today().year - 1)) + str(datetime.date.today().year)


class Hockey:
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

    def player_stats(self, ID: int, season=current_year, game_type=2):
        # request_string = "https://api-web.nhle.com/v1/player/" + str(ID) + "/landing"
        request_string = "https://api-web.nhle.com/v1/player/" + str(ID) + "/game-log/" + str(season) + "/" + str(game_type)
        string = requests.get(request_string)
        string = string.json()
        tot_secs = datetime.timedelta(minutes=0, seconds=0)
        stats = {"goals": 0, "toi": "", "points": 0, "shots": 0}
        for n in string["gameLog"]:
            stats["goals"] += int(n["goals"])
            minutes, seconds = n["toi"].split(":")
            tot_secs += datetime.timedelta(minutes=int(minutes), seconds=int(seconds))
            if "shotsAgainst" in n:
                stats["shotsAgainst"] += n["shotsAgainst"]
                stats["goalsAgainst"] += n["goalsAgainst"]
            else:
                stats["points"] += int(n["points"])
            stats["shots"] += n["shots"]
        tot_min = int(tot_secs.total_seconds()) // 60
        tot_sec = int(tot_secs.total_seconds()) % 60
        stats["toi"] = f"{tot_min}:{tot_sec:02d}"
        return stats

    def get_team(self):
        test = requests.get("https://api-web.nhle.com/v1/standings/now")
        ex = test.json()
        return ex


    # def getStats(self, player=None):
    #     print("Player:", player)
    #     players = DB.getPlayer(player)
    #     if player_info is not None:
    #         skater = [{"first": player_info[2], "last":player_info[3]}]
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

test = Hockey()
print(test.player_stats(8473533))




