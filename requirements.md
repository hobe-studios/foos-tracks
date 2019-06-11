# Requirements
1. keep track of following info for each game:   
   1. Players
   2. Score
   3. Start time
   4. End time
   5. Games played per match
2. keep track of following info for each player:
   1. Player first name
   2. Player last name
   3. Unique ID
   4. NFC ID (or something that identifies via key card)
3. persist history of all games
4. look up any game
5. see players history
6. see team stats
7. see team matchup stats
8. Player registers for access
   1. Via admin entries
   2. Via Web UI
   3. Via 1st time playing a game
9. Player joins game
   1. Manually via web UI
   2. Scans keycard
10. Foosball table tracks game info
    1. Which team scored
    2. Which team is on which side
11. UI input
    1. Start / stop game
    2. Register players
12. UI output
    1. Current game stats
    2. History graphs and such, random, scrolling
    3. History graphs and such, on demand

# EPICs

User can register as player via Web UI
- React UI for creating and showing player info
- Backend is Player Manager
- Base this on tutorial

Foosball Game Manager
- Knows players
- Knows/controls game start end
- Knows game score
- Communicates completed game data to database
- UI for starting/stopping games
- UI for seeing current game stats
	 - Players
	 - Score
	 - time

Foosball table tracks game info and reads keycards
- Instrument goals
- Instrument score LED panels
- NFC reader
- Arduino/Rasp Pi with network access for I/O

Game History Manager (Web App)
- Queryable for any game based on
 - Player/players
 - Date
 - Date range
 - Consider storing as NoSQL
- [x] Receives completed game data via REST API
- [x] Serves requests for game data via REST API

Player Manager (Web App)
- Manages user info
  - Player first name
	- Player last name
	- Unique ID
	- NFC ID (or something that identifies via key card)
- Creates users via REST API
- Updates users via REST API
- Deletes users via REST API
- Serves requests for user data via REST API

