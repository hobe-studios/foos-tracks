
# Notes

This file will be a living collection of notes captured during development of this project.

References:

https://daveceddia.com/create-react-app-express-backend   
https://treehouse.github.io/installation-guides/mac/mongo-mac.html   
https://docs.python.org/3.6/library/tk.html

## Mongdb Notes

### Starting MongoDB Daemon  

With the default db path (e.g. /data/db)   
`> mongod`   
_if this fails, read the errors, it's possible that the db path is not the default._

With a custom db path (e.g. mongodb installed from Homebrew)   
`> mongod --dbpath /usr/local/var/mongodb`

From SO Post: https://stackoverflow.com/questions/13827915/location-of-the-mongodb-database-on-mac
After installing MongoDB with Homebrew:
- The databases are stored in the /usr/local/var/mongodb/ directory
- The mongod.conf file is here: /usr/local/etc/mongod.conf
- The mongo logs can be found at /usr/local/var/log/mongodb/
- The mongo binaries are here: /usr/local/Cellar/mongodb/[version]/bin

## Game Manager UI Design

Createing a simple UI using tkinter as a POC

- Home page
  - Label "VIPER Foosball World"
  - Button "Start"

- Enter players view
  - Four text inputs
    - Team 1
      - player 1
      - player 2
    - Team 2
      - player 1
      - player 2
  - Start button

- Game stats view
  - Current time elapsed
  - Team scores

- Goal splash screen view
  - image GOAL!!
  - sound clip GOAL in spanish
