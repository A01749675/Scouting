import random

def get_info(team,metrics,df):
    info = []
    for metric in metrics:
        value = {}
        order = []
        data = {}
        for teams in range(len(df.index)):
            if df.iloc[teams]["Equipo "] == team:
                value[str(df.iloc[teams][metric])] = value.get(metric,0)+1
        for k,v in value.items():
            order.append([k,v])
        for i in range(len(order)):
            if i >0:
                data[order[i][0]] = order[i][1]*10+data[order[i-1][0]]
            else:
                data[order[i][0]] = order[i][1]*10
        info.append([metric,data])
    return(info)
#Obtiene los rangos para calcular la probabilidad
def get_prob(team,prob,metrics):
    amount = []
    count = 0
    for metric in metrics:
        if prob[count][0] == metric and metric not in ["Rank","Match","Defense","Alianza"]:
            prob_list = list(prob[count][1])
            r_value = random.randint(0,prob[count][1][prob_list[len(prob_list)-1]])
            min = 0
            for k,v in prob[count][1].items():
                if r_value > min and r_value<=v:
                    amount.append([metric,int(k)])
                min = v
        count+=1
    return amount

def scores(amount,points):
    score = 0
    fouls = 0
    mf = 0
    error = 0
    for i in range(len(amount)):
        for point in points.columns.values:
            if amount[i][0] == point and amount[i][0] not in ["Fouls","Off","Defense","Alianza"]:
                score += amount[i][1]*points.iloc[0][point]
        else:
            if amount[i][0] == "Fouls":
                fouls += amount[i][1]*points.iloc[0][point]
            if amount[i][0] == "Off":
                mf += amount[i][1]
    if len(amount) != 0 and mf != 0:
        error = mf/len(amount)
    else:
        error = 1
    score *= error
    return [score,fouls]