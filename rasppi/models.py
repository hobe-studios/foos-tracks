from gpiozero import MotionSensor
from datetime import datetime
from uuid import uuid4

class Game:
    
    team1 = None
    team2 = None
    start_time = None
    end_time = None
    finished = False

    def __init__(self, team1, team2):
        assert (team1 is not None), "Team 1 must be defined"
        assert (team2 is not None), "Team 2 must be defined"
        self.team1 = team1
        self.team2 = team2
        self.team1.score = 0
        self.team2.score = 0
        self.start_time = datetime.now()
        self.finished = False

    def get_winning_team(self):
        if self.team1.total_score() == self.team2.total_score():
            return None
        return self.team1 if self.team1.total_score() > self.team2.total_score() else self.team2 

    def get_losing_team(self):
        if self.team1.total_score() == self.team2.total_score():
            return None
        return self.team1 if self.team1.total_score() < self.team2.total_score() else self.team2

    def finish(self):
        self.finished = True
        self.end_time = datetime.now()


class Goal:

    def __init__(self, name="The goal", score_device:MotionSensor=None, score_handler=None):
        self.name = name
        self.input_device = score_device
        self.input_device.when_motion = self.scored
        self.on_score = score_handler

    def scored(self):
        self.on_score()


class Score:

    def __init__(self, scorers_name, points=1):
        self.timestamp = datetime.now
        self.scorer = scorers_name
        self.points = points


class Team:
    
    def __init__(self, name="The team", members=[], score_handler=None):
        self.id = uuid4
        self.score = 0
        self.name = name
        self.members = members # array of string of member names
        self.on_score = score_handler
        self.scores = []

    def set_on_score_handler(score_handler):
        new_score = Score(scorers_name=self.name, points=1)
        self.scores.append(new_score)
        self.on_score = score_handler

    def did_score(self):
        self.score += 1
        self.on_score()
        msg = "{0} has scored!!!\nNow has {1} points".format(self.name, self.score)
        print(msg)

    def total_score():
        total = 0
        for s in self.scores:
            total += s.points
        return total

    def reset_score():
        self.scores.clear()