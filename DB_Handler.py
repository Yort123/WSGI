import sqlite3 as sq
import API

conn = sq.connect("DB.sqlite3")

hockey = API.Hockey()
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



def get_players(team, stats=False):
    players_list = []
    players = conn.execute("select First, Last from Players where teamAbbrev = ?", (team,))
    team = players.fetchall()
    for n in team:
        print(n)
        players_list.append({"first": n[0], "last": n[1]})
    return players_list

def get_all_players(update=False):
    players = conn.execute("""select ID from Players""")
    players = players.fetchall()
    player_list = []
    for n in players:
        check = conn.execute("select * from Stats where = ?", (n[0],))
        if check is None and update:
            player_list.append(n[0])
        elif check is not None and update:
            player_list.append(n[0])
    return player_list

def update_stats():
    results = conn.execute("""select ID from Players""").fetchall()
    for n in results:
        print(n[0], "----", hockey.player_stats(n[0]))
update_stats()

