#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  score_keeper.py
#  
#  Copyright 2019  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

from gpiozero import Button, PWMLED, MotionSensor
from time import sleep
from signal import pause
from datetime import datetime


WIN_SCORE = 5


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
        if self.team1.score == self.team2.score:
            return None
        return self.team1 if self.team1.score > self.team2.score else self.team2 

    def get_losing_team(self):
        if self.team1.score == self.team2.score:
            return None
        return self.team1 if self.team1.score < self.team2.score else self.team2

    def finish(self):
        self.finished = True
        self.end_time = datetime.now()


class Goal:
    name = ""
    input_device = None
    handle_score = None
    has_scored = False

    def __init__(self, input_pin, name="The goal", score_handler=None):
        self.name = name
        self.input_device = Button(input_pin)
        self.input_device.hold_time = 0.05
        self.input_device.when_held = self.scored
        self.handle_score = score_handler

    def scored(self):
        #print("Goal scored in {0}!!".format(self.name))
        self.handle_score()


class Team:
    
    id = -1
    name = ""
    score = 0

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def scored(self):
        self.score += 1
        msg = "{0} has scored!!!\nNow has {1} points".format(self.name, self.score)
        print(msg)


def check_game(game):
    if game.team1.score >= WIN_SCORE and game.team2.score >= WIN_SCORE:
        assert False, "NOT POSSIBLE FOR BOTH TEAMS TO WIN"
    elif game.team1.score >= WIN_SCORE:
        game.finish()
    elif  game.team2.score >= WIN_SCORE:
        game.finish()


def report_game_stats(game):
    winner = game.get_winning_team()
    loser = game.get_losing_team()
    print_win_message(winning_team=winner, losing_team=loser)


def print_win_message(winning_team, losing_team):
    msg = "\n{0} has won!!!\n{0} - {1}, {2} - {3}".format(winning_team.name,
                                                        winning_team.score,
                                                        losing_team.name,
                                                        losing_team.score)
    print(msg)


def create_new_game(team1, team2):
    team1.score = 0
    team2.score = 0
    new_game = Game(team1, team2)
    return new_game


def ask_for_new_game():
    print("New game?")


def main(args):

    team1 = Team(id=1, name="Team 1")
    team2 = Team(id=2, name="Team 2")

    goal_a = Goal(input_pin=17, name="Goal A", score_handler=team1.scored)
    goal_a.assigned_team = team1

    goal_b = Goal(input_pin=18, name="Goal B", score_handler=team2.scored)
    goal_b.assigned_team = team2

    game = Game(team1=team1, team2=team2)

    while not game.finished:
        check_game(game)
        sleep(0.1)

    report_game_stats(game)
    ask_for_new_game()
    pause()


# Test main methods

def main_pwm(args):
    led = PWMLED(21)
    led.pulse()
    pause()


def handle_motion():
    print("Shake switch moved.")


def main_vib(args):
    vib = MotionSensor(16, pull_up=True)
    print("Waiting for motion ...")
    vib.when_motion = handle_motion

    #pause()

    while True:
        print(vib.value)
        sleep(0.1)


if __name__ == '__main__':
    import sys
    #main = main_vib
    sys.exit(main(sys.argv))
