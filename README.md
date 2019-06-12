# FoosTracks
System for tracking and presenting foosball game and player data

---
## Starting the app

### Backend (Express)
```bash
cd ./server
mongod --dbpath /usr/local/var/mongodb
npm start
```

### Frontend (React)
```bash
cd ./client
npm start
```
---
## Raspberry Pi
### Dependencies
```bash
sudo apt-get install python-gst-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools
```
```bash
pip3 install requests
pip3 install playsound
```