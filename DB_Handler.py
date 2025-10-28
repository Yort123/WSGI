import sqlite3 as sq
import API

conn = sq.connect("DB.sqlite3")

hockey = API.hockey()
team_list = []
abbrev_list = []

def update_players():
    Teams = conn.execute("""
    Select Abbrev from Teams
    """)
    Teams = Teams.fetchall()
    print("Updating", end="  ")
    for n in Teams:
        team = hockey.getPlayers(n[0])
        comparator = conn.execute("SELECT First, Last from Players where TeamAbbrev = ?", (n[0],))
        comparator = comparator.fetchall()
        for player in team:
            IN = False
            for i in comparator:
                if player[0] == i[0]:
                    IN = True
                    break
            if not IN:
                conn.execute("""
                INSERT INTO Players (First, Last, ID, Pos, Headshot, TeamAbbrev) VALUES (?,?,?,?,?,?)""",
                             (player[0], player[1], player[2], player[4], player[5], player[3]))
        print(".", end="")
    conn.commit()
    print("  Updated")



def get_players(team):
    players_list = []
    players = conn.execute("select First, Last from Players where teamAbbrev = ?", (team,))
    team = players.fetchall()
    for n in team:
        players_list.append({"first": n[0], "last": n[1]})
    return players_list


# print(conn.execute("""
# select * from Teams
# """).fetchall())
