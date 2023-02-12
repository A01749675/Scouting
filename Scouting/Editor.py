import tbapy as tb
tba = tb.TBA('BBUbNPzCXXsQVkaTzCgX35YMOuXPkn18MYlJFpd9japxUj4gwnNToTSMXIMSzjoz')
print(tba.event_matches("2022mxmo",keys=True))

class Robot:

    def __init__(self,TEAM):
        self.TEAM = TEAM
        self.RP = 0

    def rank(self):
        self.RP +=2


def robots(teams):
    rob = []
    for team in teams:
        robot = Robot(team)
        rob.append(robot)
    return rob

