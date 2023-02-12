import Team_info as t
import Editor as e
import BlueAlliance as ba
from operator import itemgetter
teams = []
matches = ba.event_match()


class Match:

    def __init__(self,ID):
        self.ID = 0
        self.Result = ""
    def match_result(self,Result):
        self.Result = Result

def set_match():
    match_object = []
    m = ba.total_matches()
    for i in range(1,m+1):
        match = Match(i)
        match_object.append(match)
    return match_object

def get_teams(df):
    for i in range(len(df.index)):
        team = int(str(df.iloc[i]["Equipo "]).split(" ")[0])
        if team not in teams:
            teams.append(team)
        df.at[i, "Equipo "] = team
    return teams

def game(red,blue,simulations,points,df):
    count = simulations
    vr = 0
    vb = 0
    while count>0:
        pr = t.scores(t.get_prob(red[0],t.get_info(red[0],df.columns.values[1:],df),df.columns.values[1:]),points)[0] +t.scores(t.get_prob(red[1],t.get_info(red[1],df.columns.values[1:],df),df.columns.values[1:]),points)[0]+t.scores(t.get_prob(red[2],t.get_info(red[2],df.columns.values[1:],df),df.columns.values[1:]),points)[0]
        pb = t.scores(t.get_prob(blue[0],t.get_info(blue[0],df.columns.values[1:],df),df.columns.values[1:]),points)[0] +t.scores(t.get_prob(blue[1],t.get_info(blue[1],df.columns.values[1:],df),df.columns.values[1:]),points)[0]+t.scores(t.get_prob(blue[2],t.get_info(blue[2],df.columns.values[1:],df),df.columns.values[1:]),points)[0]
        fr = t.scores(t.get_prob(red[0],t.get_info(red[0],df.columns.values[1:],df),df.columns.values[1:]),points)[1] +t.scores(t.get_prob(red[1],t.get_info(red[1],df.columns.values[1:],df),df.columns.values[1:]),points)[1] + t.scores(t.get_prob(red[2],t.get_info(red[2],df.columns.values[1:],df),df.columns.values[1:]),points)[1]
        fb = t.scores(t.get_prob(blue[0],t.get_info(blue[0],df.columns.values[1:],df),df.columns.values[1:]),points)[1]+ t.scores(t.get_prob(blue[1],t.get_info(blue[1],df.columns.values[1:],df),df.columns.values[1:]),points)[1]+ t.scores(t.get_prob(blue[2],t.get_info(blue[2],df.columns.values[1:],df),df.columns.values[1:]),points)[1]
        print(pr+fr)
        print(pb+fb)
        if pr+fr > pb+fb:
            vr +=1
        else:
            vb +=1
        count-=1
    if vr >vb:
        return ["Alianza Roja",int((vr/simulations)*100)]
    return ["Alianza Azul",int((vb/simulations)*100)]

def simulate_regional(points,df):
    robots = e.robots(teams)
    for match in matches:
        print(match)
        r = game(match[2],match[1],10,points,df)
        print(r)
        if r[0] == "Alianza Roja":
            for team in match[2]:
                for robot in robots:
                    if robot.TEAM == team:
                        robot.rank()
        else:
            for team in match[1]:
                for robot in robots:
                    if robot.TEAM == team:
                        robot.rank()

        for m in set_match():
            if m.ID == match[0]:
                m.match_result(r[0])
    return [robots,set_match()]

def view_robot(results):
    view = []
    for robot in results:
        view.append([robot.TEAM,robot.RP])
    view = sorted(view,key=itemgetter(1))
    print(view)
    return view
def view_match(results):
    view = []
    for match in results:
        view.append([match.ID,match.Result])
    view = sorted(view,key=itemgetter(0))
    return view