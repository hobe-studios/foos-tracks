#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py


import tkinter as tk


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title("VIPER Foosball World")

        # Container frame will hold all possible views we would like to show
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create app views
        self.frames = {}
        for F in (MainFrame, EnterUserFrame, GameFrame):
            frame = F(master=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
            
        self.show_frame(MainFrame)

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
        self.start_button["text"] = "Start new game"
        self.start_button["command"] = lambda: controller.show_frame(EnterUserFrame)
        self.start_button.pack(pady=10)

        self.quit = tk.Button(self,
                              text="QUIT",
                              fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom", pady=10)


class EnterUserFrame(tk.Frame):

    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.create_widgets(controller)

    def create_widgets(self, controller):
        self.team1_user1_name = tk.Label(self, text="Team 1 - Player 1")
        self.team1_user2_name = tk.Label(self, text="Team 1 - Player 2")

        self.team2_user1_name = tk.Label(self, text="Team 2 - Player 1")
        self.team2_user2_name = tk.Label(self, text="Team 2 - Player 2")

        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self)
        self.e3 = tk.Entry(self)
        self.e4 = tk.Entry(self)

        self.quit_btn = tk.Button(self, text='Quit', command=self.quit)
        self.play_btn = tk.Button(self, text='Play', command=lambda: controller.show_frame(GameFrame))

        self.team1_user1_name.grid(row=0)
        self.team1_user2_name.grid(row=1)
        self.team2_user1_name.grid(row=2)
        self.team2_user2_name.grid(row=3)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        self.quit_btn.grid(row=4, column=0, sticky=tk.W, pady=4)
        self.play_btn.grid(row=4, column=1, sticky=tk.W, pady=4)


class GameFrame(tk.Frame):
    
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        #self.create_widgets()


def main(args):
    app = App(args)
    app.mainloop()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))