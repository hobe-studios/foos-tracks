#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py

import requests
import json
from datetime import datetime

# def GameDTO:
#     def __init__(self, game):
#         self.

def send_game_history(game=None):
    url = "http://localhost:3001/games"
    payload = {
        "teams": [
            {
                "members": ["Jonny B", "Tiff Foosy"],
                "score": 5
            },
            {
                "members": ["Bobby Brown", "Whitney Houston"],
                "score": 2
            }
        ],
        "startTime": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "endTime": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }

    r = requests.post(url, data=json.dumps(payload))
    print(r)

if __name__ == '__main__':
    send_game_history()