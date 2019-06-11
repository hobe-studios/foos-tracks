
# Notes

This file will be a living collection of notes captured during development of this project.

References:

https://daveceddia.com/create-react-app-express-backend   
https://treehouse.github.io/installation-guides/mac/mongo-mac.html   


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

