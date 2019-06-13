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
from time import sleep, time
from signal import pause
from datetime import datetime, timedelta
import simpleaudio as sa
from models import Game, Goal, Team
from game_history import send_game_history
from constants import UI_GAME_CLOCK, UI_TEAM1_SCORE, UI_TEAM2_SCORE
import threading
import queue


def _play_sound_clip(sound_file, wait=False):
    wave_obj = sa.WaveObject.from_wave_file(sound_file)
    play_obj = wave_obj.play()
    if wait:
        play_obj.wait_done() 


def _get_elapsed_time_string(elapsed_seconds):
    hours, rem = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))


def _team_scored(team):
    _play_sound_clip("/home/pi/Projects/FoosTracks/resources/SoccerGoal.wav")


class AsyncMatch(threading.Thread):

    def __init__(self, ui_queue,
                team1_name, team1_members, 
                team2_name, team2_members,
                games_per_match,
                points_to_win,
                next_game_callback=None):
        super().__init__()
        self.ui_queue = ui_queue
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_members = team1_members
        self.team2_members = team2_members
        self.game_per_match = games_per_match
        self.points_to_win = points_to_win
        self.cancelled = False
        self.devices = []

    def cancel(self):
        self.cancelled = True

    def run(self):
        if not self.cancelled:
            self._start_match(self.team1_name, self.team1_members, 
                self.team2_name, self.team2_members,
                games_per_match=self.game_per_match,
                ui_queue=self.ui_queue)

    def _start_match(self, team1_name, team1_members, 
                    team2_name, team2_members,
                    games_per_match=1,
                    ui_queue=None,  # queue for asyncrohonus updates to the tkinter UI
                    next_game_callback=None):  # next_game_call_back is a function that determines whether the next game in the match should be played.  Takes no argments and returns boolean, True if game should be played, False if match shoiuld be ended.

        print("Starting match ...")

        team1 = Team(name=self.team1_name, members=self.team1_members, score_handler=_team_scored)
        team2 = Team(name=self.team2_name, members=self.team2_members, score_handler=_team_scored)

        dev = MotionSensor(16, pull_up=True, sample_rate=120, queue_len=1)
        goal_a = Goal(name="Goal A",
                    score_device=dev,
                    score_handler=None)

        dev = MotionSensor(19, pull_up=True, sample_rate=120, queue_len=1)
        goal_b = Goal(name="Goal B",
                    score_device=dev,
                    score_handler=None)

        self.devices = [goal_a.input_device, goal_b.input_device]

        games_played = 0
        while games_played < games_per_match:
            if games_played % 2 == 0:
                self._start_new_game(team1, goal_a, team2, goal_b, ui_queue=self.ui_queue)
            else:
                self._start_new_game(team1, goal_b, team2, goal_a, ui_queue=self.ui_queue)
            
            if self.cancelled:
                print("Match was cancelled")
                return

            games_played += 1

            if games_played < games_per_match:
                if next_game_callback:
                    play_next = next_game_callback()
                    if not play_next:
                        break
                else:
                    input("Press enter to play game {0} of {1} in the match ...".format(games_played+1, games_per_match))
            else:
                print("Match is over hope you had fun!")

    def _start_new_game(self, team1, goal_1, team2, goal_2, sound_fx=True, ui_queue=None):
        
        print("Starting new game ...")

        goal_1.set_on_score_handler(team1.did_score)
        goal_2.set_on_score_handler(team2.did_score)

        game = Game(team1=team1, team2=team2)
        game.start()

        if sound_fx:
            self._start_fx()

        start_time = time()
        while not game.finished:
            if self.cancelled:
                print("Game was cancelled")
                self._clean_up()
                return
            self._update_ui(ui_queue, start_time, game)
            self._check_game(game)
            sleep(0.1)

        # Game is finished
        self._report_game_stats(game)

    def _start_fx(self):
        sound_file = "/home/pi/Projects/FoosTracks/resources/SoccerCrowd.wav"
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        play_obj = wave_obj.play()

    def _stop_fx(self):
        sa.stop_all()

    def _update_ui(self, ui_queue, start_time, game):
        elapsed_time = _get_elapsed_time_string(time() - start_time)
        team1_score = game.team1.total_score()
        team2_score = game.team2.total_score()
        if ui_queue:
            ui_msg = {
                UI_GAME_CLOCK: elapsed_time,
                UI_TEAM1_SCORE: team1_score,
                UI_TEAM2_SCORE: team2_score
            }
            ui_queue.put(ui_msg)

    def _check_game(self, game):
        if game.team1.total_score() >= self.points_to_win and game.team2.total_score() >= self.points_to_win:
            assert False, "NOT POSSIBLE FOR BOTH TEAMS TO WIN"
        elif game.team1.total_score() >= self.points_to_win:
            game.finish()
        elif  game.team2.total_score() >= self.points_to_win:
            game.finish()

    def _clean_up(self):
        sa.stop_all()
        for d in self.devices:
            d.close()

    def _report_game_stats(self, game):
        winner = game.get_winning_team()
        loser = game.get_losing_team()
        send_game_history(game)
        self._print_win_message(winning_team=winner, losing_team=loser)

    def _print_win_message(self, winning_team, losing_team):
        msg = "\n{0} has won!!!\n{0} - {1}, {2} - {3}".format(winning_team.name,
                                                            winning_team.total_score(),
                                                            losing_team.name,
                                                            losing_team.total_score())
        print(msg)


def main(args):
    team1_name = "Team A"
    team2_name = "Team B"

    team1_members = ["Jonny B", "Tiffy Monster"]
    team2_members = ["Otis Spunky", "Broomhilda Grimp"]

    start_match(team1_name=team1_name, team1_members=team1_members, team2_name=team2_name, team2_members=team2_members)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
