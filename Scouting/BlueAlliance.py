import tbapy
import matplotlib.pyplot as plt
from operator import itemgetter
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def b_ranking():
    blue_team = []
    tba = tbapy.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
    details = tba.event_rankings("2022mxmo")
    print(details["rankings"])
    for detail in details["rankings"]:
        blue_team.append([detail["rank"],int(detail["team_key"][3:]),int(detail["record"]["wins"]),int(detail["matches_played"])])
    return blue_team
def team_match(team):
    info = []
    tba = tbapy.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
    details = tba.team_matches(team,"2022mxmo",keys=False)
    for detail in details:
        blue = []
        red = []
        for i in range(3):
            if detail["comp_level"] == "qm":
                blue.append(detail["alliances"]["blue"]["team_keys"][i][3:])
                red.append(detail["alliances"]["red"]["team_keys"][i][3:])
        if detail["comp_level"] == "qm":
            info.append([detail["match_number"],blue,red])
    info = sorted(info,key=itemgetter(0))
    return info
def event_match():
    matches = []
    tba = tbapy.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
    details = tba.event_matches("2022mxmo",keys=False)
    for detail in details:
        blue = []
        red = []
        for i in range(3):
            blue.append(int(detail["alliances"]["blue"]["team_keys"][i][3:]))
            red.append(int(detail["alliances"]["red"]["team_keys"][i][3:]))
        if detail["comp_level"]=="qm":
            matches.append([detail["match_number"],blue,red])
    return matches

def total_matches():
    matches = []
    tba = tbapy.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
    details = tba.event_matches("2022mxmo",keys=False)
    for detail in details:
        if detail["comp_level"]=="qm":
            matches.append(detail["match_number"])
    return max(matches)

def learning(event):
    tba = tbapy.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
    details = tba.event_matches(event,keys=False)
    info = []
    x = []
    y = []
    for detail in details:
        if detail["comp_level"] == "qm":
            sum = (int(detail["alliances"]["blue"]["score"]) +int(detail["alliances"]["red"]["score"]))/2
            info.append([int(detail["match_number"]),sum])
    info = sorted(info,key=itemgetter(0))
    count = 0
    for i in info:
        x.append(i[0])
        y.append(i[1])
        count += 1
    plt.plot(x,y)
    plt.show()
def curve(team,event,window):
    tba = tbapy.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
    details = tba.team_matches(team,event,keys=False)
    scores = []
    x = []
    y = []
    for detail in details:
        blue = detail["alliances"]["blue"]["team_keys"]
        red = detail["alliances"]["red"]["team_keys"]
        if "frc"+str(team) in blue:
            scores.append([detail["match_number"],detail["alliances"]["blue"]["score"]])
            print("x")
        else:
            scores.append([detail["match_number"], detail["alliances"]["red"]["score"]])
            print("y")
    scores = sorted(scores,key=itemgetter(0))
    for i in scores:
        x.append(i[0])
        y.append(i[1])
    figure = plt.figure(figsize=(5, 4), dpi=70)
    figure.add_subplot(111).plot(x,y)
    plt.xlabel("Match")
    plt.ylabel("Score")
    plt.title("Match results")
    chart = FigureCanvasTkAgg(figure, window)
    chart.get_tk_widget().place(x=450, y=50)
    plt.grid()


