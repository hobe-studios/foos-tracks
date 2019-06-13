#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py


import tkinter as tk
from queue import Queue, Empty
from score_keeper import AsyncMatch
from constants import UI_GAME_CLOCK, UI_TEAM1_SCORE, UI_TEAM2_SCORE


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._create_ui()
        self._set_up_async_queue()

    def _create_ui(self):
        self.title("VIPER Foosball World")

        # Container frame will hold all possible views we would like to show
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create app views
        self.frames = {}
        for F in (MainFrame, MatchSetupFrame, MatchFrame):
            frame = F(master=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
            
        self.show_frame(MainFrame)

    def _set_up_async_queue(self):
        self.queue = Queue()
        self.after(100, self._process_queue)

    def _process_queue(self):
        try:
            msg = self.queue.get(0)

            # msg should be a dictionary with key value pairs, specifying what UI elements to update
            for ui_elem, value in msg.items():
                if ui_elem == UI_GAME_CLOCK:
                    self.frames[MatchFrame].set_game_time(value)
                elif ui_elem == UI_TEAM1_SCORE:
                    self.frames[MatchFrame].set_team1_score(value)
                elif ui_elem == UI_TEAM2_SCORE:
                    self.frames[MatchFrame].set_team2_score(value)

        except Empty:
            pass

        self.after(100, self._process_queue)

    def show_frame(self, frame):
        self.frames[frame].tkraise()


class MainFrame(tk.Frame):
    
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.create_widgets(controller)

    def create_widgets(self, controller):
        self.head_label = tk.Label(self)
        self.head_label["text"] = "Welcome to VIPER Foosball World!!"        
        self.head_label.pack(side="top", pady=10)

        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start a new match"
        self.start_button["command"] = lambda: controller.show_frame(MatchSetupFrame)
        self.start_button.pack(side="bottom", pady=10)


class MatchSetupFrame(tk.Frame):

    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):

        self.team1_label = tk.Label(self, text="Team 1")
        self.team2_label = tk.Label(self, text="Team 2")

        self.team1_user1_name = tk.Label(self, text="Player 1")
        self.team1_user2_name = tk.Label(self, text="Player 2")

        self.team2_user1_name = tk.Label(self, text="Player 1")
        self.team2_user2_name = tk.Label(self, text="Player 2")

        self.team1_text = tk.Entry(self)
        self.team2_text = tk.Entry(self)
        self.team1_player1_text = tk.Entry(self)
        self.team1_player2_text = tk.Entry(self)
        self.team2_player1_text = tk.Entry(self)
        self.team2_player2_text = tk.Entry(self)

        self.number_games_label = tk.Label(self, text="Games per match")
        self.number_games_text = tk.Entry(self)
        self.number_games_text.insert(0, "3")

        self.win_points_label = tk.Label(self, text="Points needed to win")
        self.win_points_text = tk.Entry(self)
        self.win_points_text.insert(0, "5")

        self.create_match_btn = tk.Button(self, text='Create Match', command=self.show_match_frame)

        self.team1_label.grid(row=0, column=0)
        self.team1_text.grid(row=0, column=1)
        self.team2_label.grid(row=0, column=2)
        self.team2_text.grid(row=0, column=3)

        self.team1_user1_name.grid(row=1, column=0)
        self.team1_user2_name.grid(row=2, column=0)

        self.team1_player1_text.grid(row=1, column=1)
        self.team1_player2_text.grid(row=2, column=1)

        self.team2_user1_name.grid(row=1, column=2)
        self.team2_user2_name.grid(row=2, column=2)

        self.team2_player1_text.grid(row=1, column=3)
        self.team2_player2_text.grid(row=2, column=3)

        self.number_games_label.grid(row=3, column=0, pady=10)
        self.number_games_text.grid(row=3, column=1, pady=10)

        self.win_points_label.grid(row=3, column=2, pady=10)
        self.win_points_text.grid(row=3, column=3, pady=10)

        self.create_match_btn.grid(row=4, column=1, sticky=tk.W, pady=10)


    def show_match_frame(self):
        team1_name = self.team1_text.get()
        team2_name = self.team2_text.get()

        team1_members = [self.team1_player1_text.get(), self.team1_player2_text.get()] 
        team2_members = [self.team2_player1_text.get(), self.team2_player2_text.get()]

        games_per_match = int(self.number_games_text.get())
        win_points = int(self.win_points_text.get())

        match_frame = self.controller.frames[MatchFrame]
        match_frame.set_match_info(team1_name, team1_members, team2_name, team2_members, games_per_match, win_points)
        self.controller.show_frame(MatchFrame)


class MatchFrame(tk.Frame):
    
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller

        self.team1_name = tk.StringVar()
        self.team1_members = []
        self.team1_score = tk.IntVar()
        
        self.team2_name = tk.StringVar()
        self.team2_members = []
        self.team2_score = tk.IntVar()

        self.game_clock = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        self.team1_name_label = tk.Label(self, text="", textvariable=self.team1_name)
        self.team2_name_label = tk.Label(self, text="", textvariable=self.team2_name)

        self.team1_score_label = tk.Label(self, text="", textvariable=self.team1_score)
        self.team2_score_label = tk.Label(self, text="", textvariable=self.team2_score)

        self.game_clock_label = tk.Label(self, text="", textvariable=self.game_clock)

        self.cancel_btn = tk.Button(self, text="Cancel", command=self._quit_match)
        self.start_btn = tk.Button(self, text="Start", command=self._start_match)

        self.team1_name_label.grid(row=0, column=0)
        self.team1_score_label.grid(row=1, column=0)
        self.team2_name_label.grid(row=0, column=1)
        self.team2_score_label.grid(row=1, column=1)

        self.game_clock_label.grid(row=2, column=0)

        self.cancel_btn.grid(row=3, column=0, sticky=tk.W, pady=4)
        self.start_btn.grid(row=3, column=1, sticky=tk.W, pady=4)

    def set_match_info(self, team1_name, team1_members, team2_name, team2_members, games_per_match, win_points):
        self.team1_name.set(team1_name)
        self.team2_name.set(team2_name)

        self.team1_members = team1_members
        self.team2_members = team1_members

        self.games_per_match = games_per_match
        self.win_points = win_points

    def _start_match(self):
        self.team1_score.set(0)
        self.team2_score.set(0)
        self.game_clock.set("00:00:00")

        self.match = AsyncMatch(self.controller.queue,
            self.team1_name.get(), self.team1_members,
            self.team2_name.get(), self.team2_members,
            self.games_per_match, self.win_points
        )
        self.match.start()

    def _quit_match(self):
        self.match.cancel()

    def set_game_time(self, game_time):
        self.game_clock.set(game_time)

    def set_team1_score(self, score):
        self.team1_score.set(score)

    def set_team2_score(self, score):
        self.team2_score.set(score)


def main(args):
    app = App(args)
    app.mainloop()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))