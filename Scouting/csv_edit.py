import pandas as pd
import csv
import General as g

def order(df):
    for i in range(len(df.index)):
        if df.iloc[i]["Auto_Line"] == "Si":
            df.at[i,"Auto_Line"] = 1
        else:
            df.at[i,"Auto_Line"] = 0
        if df.iloc[i]["Defense"] == "Si":
            df.at[i,"Defense"]=1
        else:
            df.at[i,"Defense"]=0
def general_stats(team, metrics,df,points):
    stats = [team]
    count = 0
    for metric in metrics:
        sum = 0
        value = 0
        pos = 0
        min = 81
        matches = 0
        defense = 0
        for i in range(len(df.index)):
            if team == int(df.iloc[i]["Equipo "]) and metric not in ["Off","Rank","Match","Defense","Alianza"]:
                sum += i
                for point in points.columns.values:
                    if metric == point:
                        value+= df.iloc[i][metric]*i*points.iloc[0][point]

            elif metric == "Off" and team == df.iloc[i]["Equipo "]:
                value+= df.iloc[i][metric]
                sum=1
            elif metric == "Rank" and team == df.iloc[i]["Equipo "] :
                if int(df.iloc[i]["Match"])<min:
                    min = int(df.iloc[i]["Match"])
                    pos = i
            elif metric == "Match" and team == df.iloc[i]["Equipo "]:
                matches +=1
            elif metric == "Defense" and team == df.iloc[i]["Equipo "]:
                defense+=1
        if sum != 0 and metric not in ["Rank","Match","Alianza","Defense"]:
            stats.append(int(value/sum))
        elif metric not in ["Rank","Match","Defense","Alianza"]:
            stats.append(0)
        elif metric == "Rank":
            stats.append(df.iloc[pos]["Rank"])
        elif metric == "Match":
            stats.append(matches)
        elif metric == "Defense":
            stats.append(defense)

        count+=1
    stats.append(g.quantify(team,stats,df))
    print(stats)
    return stats

def ranking(teams,csv1,df,metrics,points):
    stats = []
    header = list(df.columns.values)
    header.append("Value")
    header.pop(header.index("Alianza"))
    for team in teams:
        stats.append(general_stats(team,metrics,df,points))
    with open(csv1,"w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(stats)
    return (pd.read_csv(csv1))
#Permite filtrar el ranking
def order_rank(criterion,csv1,ascendente,teams,metrics,df,points):
    rank = ranking(teams,csv1,df,metrics,points)
    rank.sort_values([criterion],axis=0, ascending=ascendente,inplace=True)
    return (rank)
#Obtiene un csv con los mejores equipos
def best_alliance(team,csv1,metrics,teams):
    t_stats = general_stats(team,metrics)
    t_value = t_stats[len(t_stats)-1]
    t_rank = t_stats[len(t_stats)-2]
    possible_teams = []
    ranking(teams,csv1)
    db = pd.read_csv(csv1)
    value = 0
    for i in range(len(db.index)):
        value+=int(db.iloc[i]["Value"])
    avg = int(value/len(teams))
    for i in range(len(db.index)):
        if int(db.iloc[i]["Value"])>avg and db.iloc[i]["Equipo "] != team and db.iloc[i]["Rank"]> t_rank:
            possible_teams.append(db.iloc[i]["Equipo "])
    order_rank("Value",csv1,False,possible_teams)