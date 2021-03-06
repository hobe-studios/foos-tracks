# -*- coding: utf-8 -*-
#
#  game_history.py


import requests
import json
from datetime import datetime
from models import Game, Team, Score


class DataTransferObject:
    def __init__(self):
        pass

    def toJSON(self):
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__)


class ScoreDTO(DataTransferObject):
    def __init__(self, score:Score):
        super().__init__()
        self.points = score.points
        self.scorer = score.scorer
        self.timestamp = score.timestamp.strftime("%Y/%m/%d, %H:%M:%S")


class TeamDTO(DataTransferObject):
    def __init__(self, team:Team):
        super().__init__()
        self.members = team.members
        self.scores = [ ScoreDTO(s) for s in team.scores ] 
        self.score = team.total_score()
        self.name = team.name


class GameDTO(DataTransferObject):
    def __init__(self, game:Game):
        super().__init__()
        self.startTime = game.start_time.strftime("%Y/%m/%d/, %H:%M:%S")
        self.endTime = game.end_time.strftime("%Y/%m/%d, %H:%M:%S")
        self.teams = [TeamDTO(game.team1), TeamDTO(game.team2)]


def send_game_history(game:Game):
    url = "http://192.168.10.:3001/games"
    gameDTO = GameDTO(game)
    payload = json.loads(gameDTO.toJSON())
    print("Saving game results ...")
    r = requests.post(url, json=payload, timeout=5)
