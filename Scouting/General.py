import pandas as pd
from operator import itemgetter

#VALOR
def quantify(team,stats,df):
    mf = 0
    fouls = 0
    defense = 0
    count = 0
    drate = 0
    for i in range(len(df.index)):
        if df.iloc[i]["Equipo "]==team:
            count+=1
            mf+=df.iloc[i]["Off"]
            defense += df.iloc[i]["Defense"]
            fouls += df.iloc[i]["Fouls"]*2

    points = 0
    for i in range(2,len(stats)-1):
        points+=stats[i]
        print(points)
    if mf != 0:
        points*=(1-mf/count)
        print(points)
    if defense != 0:
        drate = int(fouls/defense)
    return int(points+drate)
def errors(team,df):
    mf = 0
    count = 0
    for i in range(len(df.index)):
        if df.iloc[i]["Equipo "]==team:
            count+=1
            mf+=df.iloc[i]["Off"]
    return (str(mf/count*100)+"%")
def progression(team,df,metrics,points):
    x = []
    y=[]
    p = []
    for i in range(len(df.index)):
        value = 0
        if df.iloc[i]["Equipo "] == team:
            for metric in metrics:
                if metric not in ["Off","Rank","Match","Defense","Equipo ","Alianza","Fouls"]:
                    for point in points.columns.values:
                        if metric == point:
                            print(metric)
                            print(points.iloc[0][point])
                            print(int(df.iloc[i][metric]))
                            value += int(df.iloc[i][metric]) * points.iloc[0][point]
                            print(value)
            p.append([df.iloc[i]["Match"],value])
    p = sorted(p,key=itemgetter(0))
    for i in range(len(p)):
        x.append(p[i][0])
        y.append(p[i][1])
    print(y)
    return[x,y,max(y),sum(y)/len(y)]