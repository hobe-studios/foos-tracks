#!/usr/bin/env python3
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
import simpleaudio as sa
from models import Game, Goal, Team

WIN_SCORE = 5

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


def play_sound_clip(sound_file, wait=False):
    wave_obj = sa.WaveObject.from_wave_file(sound_file)
    play_obj = wave_obj.play()
    if wait:
        play_obj.wait_done() 


def main(args):

    team_scored = lambda: play_sound_clip("/home/pi/Projects/FoosTracks/resources/SoccerGoal.wav")

    team1 = Team(id=1, name="Team 1", score_handler=team_scored)
    team2 = Team(id=2, name="Team 2", score_handler=team_scored)

    dev = MotionSensor(16, pull_up=True, sample_rate=60, queue_len=3)
    goal_a = Goal(name="Goal A",
                  score_device=dev,
                  score_handler=team1.scored)
    goal_a.assigned_team = team1

    dev = MotionSensor(18, pull_up=True, sample_rate=60, queue_len=3)
    goal_a = Goal(name="Goal B",
                  score_device=dev,
                  score_handler=team1.scored)

    print("Starting game!")

    game = Game(team1=team1, team2=team2)

    play_sound_clip("/home/pi/Projects/FoosTracks/resources/SoccerCrowd.wav")

    while not game.finished:
        check_game(game)
        sleep(0.1)

    report_game_stats(game)
    ask_for_new_game()
    pause()

# # Test main methods

# def main_pwm(args):
#     led = PWMLED(21)
#     led.pulse()
#     pause()


# def handle_motion():
#     print("Shake switch moved.")


# def main_vib(args):
#     vib = MotionSensor(16, pull_up=True)
#     print("Waiting for motion ...")
#     vib.when_motion = lambda: print("Shake switch moved.") #handle_motion

#     #pause()

#     while True:
#         print(vib.value)
#         sleep(0.1)


# def main_play_sound(args):
#     print("Gonna play sound ...")
#     sound_file = "/home/pi/Projects/FoosTracks/resources/SoccerCrowd.wav"
#     wave_obj = sa.WaveObject.from_wave_file(sound_file)
#     play_obj = wave_obj.play()
#     print("Should be playing sound ...")
#     play_obj.wait_done()


if __name__ == '__main__':
    import sys
    #main = main_play_sound
    #main = main_vib
    sys.exit(main(sys.argv))
