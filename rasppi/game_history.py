# -*- coding: utf-8 -*-
#
#  game_history.py


import requests
import json
from datetime import datetime
from models import Game, Team


class DataTransferObject:
    def __init__(self):
        pass

    def toJSON(self):
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__)


class TeamDTO(DataTransferObject):
    def __init__(self, team:Team):
        super().__init__()
        self.members = team.members
        self.score = team.score


class GameDTO(DataTransferObject):
    def __init__(self, game:Game):
        super().__init__()
        self.start_time = game.start_time.strftime("%Y/%m/%d/, %H:%M:%S")
        self.end_time = game.end_time.strftime("%Y%m/%d, %H:%M:%S")
        self.teams = [TeamDTO(game.team1), TeamDTO(game.team2)]


def send_game_history(game:Game):
    url = "http://192.168.1.10:3001/games"
    gameDTO = GameDTO(game)
    payload = json.loads(gameDTO.toJSON())
    r = requests.post(url, json=payload)
    print(r.json)


def main():
    team1 = Team(name="A", members=["Jill", "Jack"])
    team2 = Team(name="B", members=["Bod", "Bonnie"])
    game = Game(team1, team2)
    game.finish()
    send_game_history(game)


if __name__ == '__main__':
    main()