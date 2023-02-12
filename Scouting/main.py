# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import random
import requests
import tbapy
import csv
import tkinter as tk
import json
import Editor as ed
from urllib.request import urlopen
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from operator import itemgetter
import BlueAlliance as ba
import General as g
import csv_edit as c
import Team_info as t
import Simulations as s
df = pd.read_csv("quals.csv", encoding='latin-1')
points = pd.read_csv("scores.csv")
global count
count = True
teams = s.get_teams(df)
metrics = df.columns.values[1:]
c.order(df)

window = tk.Tk("Main")
window.geometry("1000x800")
window.configure(bg='black')
Canvas = tk.Canvas(window,height=500,width=1100,bg="black")
Canvas.pack(pady=30)
Canvas.create_rectangle(790,0,798,600,fill="white")
Label = tk.Label(window,text="New Scouting. The future is now.",font=("Arial", 14, "bold"),fg="blue",bg="black",width=30,height=3)
Label.place(x=-20,y=-30)
L2 = tk.Label(window,text="Next Gen Stats: Buluk",font=("TimesNewRoman", 14, "bold"),fg="green",bg="white",width=30,height=2)
L2.place(x=0,y=30)
L3 = tk.Label(window,text="Equipo: 3472",font=("TimesNewRoman", 10, "bold"),fg="green",bg="white",width=30,height=2)
L3.place(x=0,y=100)
L4 = tk.Label(window,text = "Net Value: "+str(c.general_stats(3472,metrics,df,points)[-1]),font=("TimesNewRoman", 10, "bold"),fg="green",bg="white",width=30,height=2)
L4.place(x=0,y=150)
L5 = tk.Label(window,text = "PPG: "+str(g.progression(3472,df,metrics,points)[3]),font=("TimesNewRoman", 10, "bold"),fg="green",bg="white",width=30,height=2)
L5.place(x=0,y=200)
L6 = tk.Label(window,text = "MAX Score: "+str(g.progression(3472,df,metrics,points)[2]),font=("TimesNewRoman", 10, "bold"),fg="green",bg="white",width=30,height=2)
L6.place(x=0,y=250)
L7 = tk.Label(window,text = "Error percentage: "+g.errors(3472,df),font=("TimesNewRoman", 10, "bold"),fg="green",bg="white",width=30,height=2)
L7.place(x=0,y=300)
figure = plt.figure(figsize=(5, 4), dpi=60)
figure.add_subplot(111).plot(g.progression(3472,df,metrics,points)[0],g.progression(3472,df,metrics,points)[1])
plt.xlabel("Match")
plt.ylabel("Score")
plt.title("Match results")
chart = FigureCanvasTkAgg(figure, window)
chart.get_tk_widget().place(x=450,y=50)
plt.grid()

def view():
    global count
    if count:
        count = False
        print(count)
        return True
    else:
        count = True
        return False
def wTable():
    window2 = tk.Tk("Ranking")
    window2.geometry("900x500")
    window2.configure(bg='black')
    criterion = tk.Text(window2,width=14,height=2)
    criterion.place(x=750,y=50)
    ascendente = view()
    db = c.ranking(teams,"rank1.csv",df,metrics,points)
    Title = db.columns.values
    columns = len(db.columns.values)
    rows = len(db.index)
    for i in range(columns):
        e = tk.Entry(window2, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
        e.grid(row=0, column=i)
        e.insert(1, Title[i])
    for i in range(1,rows+1):
        for j in range(columns):
            e = tk.Entry(window2, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
            e.grid(row=i, column=j)
            e.insert(1, db.iloc[i-1][j])
    def worder(window2,criterion,ascendente,teams):
        ascendente = view()
        db = c.order_rank(criterion, "rank1.csv", ascendente, teams,metrics,df,points)
        Title = db.columns.values
        columns = len(db.columns.values)
        rows = len(db.index)
        for i in range(columns):
            e = tk.Entry(window2, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
            e.grid(row=0, column=i)
            e.insert(0, Title[i])
        for i in range(1, rows+1):
            for j in range(columns):
                e = tk.Entry(window2, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
                e.grid(row=i, column=j)
                e.insert(0, db.iloc[i-1][j])
    b2 = tk.Button(window2,text="Sort Teams",bg="blue",width=15,height=2,command = lambda m="F":worder(window2,criterion.get("1.0","end-1c"),ascendente,teams))
    b2.place(x=750,y=0)

def wScore():
    window = tk.Tk("Simulation")
    window.geometry("350x300")
    window.configure(bg="black")
    Canvas = tk.Canvas(window, height=350, width=300, bg="black")
    Canvas.pack(pady=30)
    Canvas.create_rectangle(200, 0, 205, 300, fill="white")
    tx = tk.Text(window,width=14,height=3)
    tx.place(x=60,y=100)
    def score(team):
        value = t.scores(t.get_prob(team, t.get_info(team, metrics,df), metrics),points)
        L = tk.Label(window, text="Score: " + str(int(value[0])), font=("Arial", 12, "bold"),fg="green", bg="black", width=9, height=2)
        L.place(x=229, y=50)
        sum = 0
        s =[]
        for i in range(10):
            value = t.scores(t.get_prob(team, t.get_info(team, metrics,df), metrics),points)
            sum+=value[0]
            s.append(value[0])
        L1 = tk.Label(window, text="Max: " + str(max(s)), font=("Arial", 12, "bold"),fg="green", bg="black", width=9, height=2)
        L1.place(x=229, y=100)
        L2 = tk.Label(window, text="Avg: " + str(int(sum/10)), font=("Arial", 12, "bold"),fg="green", bg="black", width=9, height=2)
        L2.place(x=229, y=150)

    b = tk.Button(window,text="Calculate",bg="blue",width=15,height=3,command = lambda m = "F": score(int(tx.get("1.0","end-1c"))))
    b.place(x=60,y=33)

def wGame():
    window = tk.Tk("Game Simulator")
    window.geometry("600x400")
    window.configure(bg="black")
    Canvas = tk.Canvas(window, height=400, width=600, bg="black")
    Canvas.pack(pady=0)
    Canvas.create_rectangle(205, 0, 210, 600, fill="white")
    l1 = tk.Label(window,text ="Alianza Roja",width=11,height=2)
    l1.place(x=0,y=20)
    t = tk.Text(window,width=10,height=2)
    t.place(x=0,y=60)
    t1 = tk.Text(window,width=10,height=2)
    t1.place(x=0,y=120)
    t2 = tk.Text(window,width=10,height=2)
    t2.place(x=0,y=180)
    l1 = tk.Label(window,text ="Alianza Azul",width=11,height=2)
    l1.place(x=120,y=20)
    t3 = tk.Text(window,width=10,height=2)
    t3.place(x=120,y=60)
    t4 = tk.Text(window,width=10,height=2)
    t4.place(x=120,y=120)
    t5 = tk.Text(window,width=10,height=2)
    t5.place(x=120,y=180)
    t6 = tk.Text(window,width=10,heigh=3)
    t6.place(x=60,y=220)
    def games():
        result = s.game([int(t.get("1.0","end-1c")),int(t1.get("1.0","end-1c")),int(t2.get("1.0","end-1c"))],[int(t3.get("1.0","end-1c")),int(t4.get("1.0","end-1c")),int(t5.get("1.0","end-1c"))],int(t6.get("1.0","end-1c")),points,df)
        label = tk.Label(window,text=str(result),font=("Arial", 15, "bold"),width=30,height=3,bg="black",fg="green")
        label.place(x=210,y=150)
    button = tk.Button(window,text="Simulate",bg="blue",width=10,height=2,command = lambda m = "F":games())
    button.place(x=60,y=300)
def wRanking():
    window = tk.Tk()
    window.geometry("720x500")
    window.configure(bg="black")
    df = ba.b_ranking()
    Title = ["Rank","Team","Wins","Matches"]
    columns = len(Title)
    rows = len(df)
    def table(Title,columns,rows,df):
        for i in range(columns):
            e = tk.Entry(window, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
            e.grid(row=0, column=i)
            e.insert(0, Title[i])
        for i in range(1, rows+1):
            for j in range(columns):
                e = tk.Entry(window, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
                e.grid(row=i, column=j)
                e.insert(0, df[i-1][j])
    b = tk.Button(window,text="Calculate",bg="blue",width=15,height=3,command = lambda m = "F": table(Title,columns,rows,df))
    b.place(x=300,y=33)

def wMatch():
    window = tk.Tk()
    window.geometry("600x600")
    window.configure(bg="black")
    label = tk.Label(window,width=10,height=2,text="Team",bg="black",fg="white")
    label.place(x=400,y=50)
    text = tk.Text(window, width=10, height=5)
    text.place(x=400, y=100)
    def table(window,text):
        data = ba.team_match(int(text.get("1.0", "end-1c")))
        titles = ["Match", "Blue Teams", "Red Teams"]
        for i in range(len(titles)):
            e = tk.Entry(window, width=21, bg="grey", fg="blue", font=("Arial", 7, "bold"))
            e.grid(row=0,column=i)
            e.insert(0,titles[i])
        for i in range(1,len(data)+1):
            for j in range(len(data[1])):
                e = tk.Entry(window,width=21, bg="grey", fg="blue", font=("Arial", 7, "bold"))
                e.grid(row=i,column=j)
                e.insert(0,data[i-1][j])
    Button = tk.Button(window,text="See Match",width=15,height=3,bg="blue",command = lambda m="F":table(window,text))
    Button.place(x=400,y=200)

def wSimulation():
    window = tk.Tk()
    window.geometry("1000x800")
    window.configure(bg="black")
    def sim():
        results = s.simulate_regional(points, df)
        teams_rank = s.view_robot(results[0])
        Title = ["Team", "RP"]
        for i in range(len(Title)):
            e = tk.Entry(window, width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
            e.grid(row=0,column=i)
            e.insert(0,Title[i])
        for i in range(len(teams_rank[0])):
            for j in range(1,len(teams_rank)+1):
                e = tk.Entry(window,width=10, bg="grey", fg="blue", font=("Arial", 7, "bold"))
                e.grid(row=j,column=i)
                e.insert(0,teams_rank[j-1][i])
    Button = tk.Button(window,text="See Match",width=15,height=3,bg="blue",command = lambda m="F":sim())
    Button.place(x=300,y=200)

def BlueAllianceData():
    window = tk.Tk()
    window.geometry("800x800")
    window.configure(bg="black")
    Label = tk.Label(window,text="Equipo",width=10,height=3,bg="black",fg="white")
    Label.place(x=50,y=50)
    Text = tk.Text(window, width=10,height=3)
    Text.place(x=50,y=100)
    Label2 = tk.Label(window,text="Regional",width=10,height=3,bg="black",fg="white")
    Label2.place(x=150,y=50)
    Text_2 = tk.Text(window, width=10,height=3)
    Text_2.place(x=150, y=100)
    Label3 = tk.Label(window,text="Match",width=10,height=3,bg="black",fg="white")
    Label3.place(x=520,y=17)
    Button = tk.Button(window,text="BA Progression",width=15,height=3,bg="blue",fg="white",command= lambda M = "F":ba.curve(int(Text.get("1.0", "end-1c")),Text_2.get("1.0","end-1c"),window))
    Button.place(x=90,y=155)

def teamOverview():
    window = tk.Tk("Main")
    window.geometry("1000x800")
    window.configure(bg='black')
    Canvas = tk.Canvas(window, height=500, width=1100, bg="black")
    Canvas.pack(pady=30)
    Canvas.create_rectangle(790, 0, 798, 600, fill="white")
    text = tk.Text(window,width=14,height=3)
    text.place(x=799,y=100)
    def getstats(team):
        L2 = tk.Label(window, text="Next Gen Stats: "+team, font=("TimesNewRoman", 14, "bold"), fg="green", bg="white",
                      width=30, height=2)
        L2.place(x=0, y=30)
        L3 = tk.Label(window, text="Equipo: "+team, font=("TimesNewRoman", 10, "bold"), fg="green", bg="white", width=30,
                      height=2)
        L3.place(x=0, y=100)
        L4 = tk.Label(window, text="Net Value: " + str(c.general_stats(int(team), metrics, df, points)[-1]),
                      font=("TimesNewRoman", 10, "bold"), fg="green", bg="white", width=30, height=2)
        L4.place(x=0, y=150)
        L5 = tk.Label(window, text="PPG: " + str(g.progression(int(team), df, metrics, points)[3]),
                      font=("TimesNewRoman", 10, "bold"), fg="green", bg="white", width=30, height=2)
        L5.place(x=0, y=200)
        L6 = tk.Label(window, text="MAX Score: " + str(g.progression(int(team), df, metrics, points)[2]),
                      font=("TimesNewRoman", 10, "bold"), fg="green", bg="white", width=30, height=2)
        L6.place(x=0, y=250)
        L7 = tk.Label(window, text="Error percentage: " + g.errors(int(team), df), font=("TimesNewRoman", 10, "bold"),
                      fg="green", bg="white", width=30, height=2)
        L7.place(x=0, y=300)
        figure = plt.figure(figsize=(5, 4), dpi=60)
        figure.add_subplot(111).plot(g.progression(int(team), df, metrics, points)[0],
                                     g.progression(int(team), df, metrics, points)[1])
        plt.xlabel("Match")
        plt.ylabel("Score")
        plt.title("Match results")
        chart = FigureCanvasTkAgg(figure, window)
        chart.get_tk_widget().place(x=450, y=50)
        plt.grid()
    Button = tk.Button(window,text="Get Stats",width=15,height=3,bg="blue",fg="white",command= lambda M = "F":getstats(text.get("1.0", "end-1c")))
    Button.place(x=799,y=150)

button2 = tk.Button(window,text="Simulate Score",bg="blue",width=27,height=2,command =lambda m="F":wScore())
button2.place(x=799,y=52)
button3 = tk.Button(window,text="Simulate Game",bg="blue",width=27,height=2,command =lambda m="F":wGame())
button3.place(x=799,y=102)
button = tk.Button(window,text="Ranking",bg="blue",width=27,height=2,command =lambda m="F":wTable())
button.place(x=799,y=202)
button5 = tk.Button(window,text="Matches",bg="blue",width=27,height=2,command = lambda m="F":wMatch())
button5.place(x=799,y=252)
button6 = tk.Button(window,text="Simulate Regional",bg="blue",width=27,height=2,command = lambda m="F":wSimulation())
button6.place(x=799,y=152)
button4 = tk.Button(window,text="Ranking Blue Alliance",bg="blue",width=27,height=2,command =lambda m="F":wRanking())
button4.place(x=799,y=302)
button7 = tk.Button(window,text="Blue Alliance Stats",bg="blue",width=27,height=2,command =lambda m="F":BlueAllianceData())
button7.place(x=799,y=352)
button8 = tk.Button(window,text="Team Overview",bg="blue",width=27,height=2,command =lambda m="F":teamOverview())
button8.place(x=799,y=402)


window.mainloop()
