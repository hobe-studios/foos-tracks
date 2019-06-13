var mongoose = require('mongoose');
var Game = mongoose.model('Game');

module.exports.gamesGetAll = function(req, res) {
    
    var offset = 0;
    var count = 100;
    var maxCount = 100;
    
    if (req.query && req.query.offset) {
        offset = parseInt(req.query.offset, 10);
    }
    if (req.query && req.query.count) {
        count = parseInt(req.query.count, 10);
    }
    
    // Validate query params
    if (isNaN(offset) || isNaN(count)) {
        res
        .status(400)
        .json({
            "message": "If supplied in query string, offset and count should be integers."
        });
        return;
    }
    
    if (count > maxCount) {
        res
        .status(400)
        .json({
            'message': 'Count limit of ' + maxCount + " exceeded"
        });
        return;
    }
    
    Game
    .find()
    .skip(offset)
    .limit(count)
    .exec(function(err, games) {
        if (err) {
            console.log('Error finding games');
            res
            .status(500)
            .json(err);
        } else {
            console.log('Found games', games.length);
            res
            .status(200)
            .json(games);
        }
    });
    
};

module.exports.gamesGetOne = function(req, res) {
    
    var gameId = req.params.gameId;
    console.log("GET the game id " + gameId);
    
    Game
    .findById(gameId)
    .exec(function(err, doc) {
        
        var response = {
            'status': 200,
            'message': doc
        };
        
        if (err) {
            console.log('Error finding a game');
            response.status = 500;
            response.message = err;
        } else if (!doc) {
            console.log('Game id not found in database: ', gameId);
            response.status = 404;
            response.message = {
                message: 'Game ID not found ' + gameId
            };
        }
        
        res
        .status(response.status)
        .json(response.message);
        
    });
};

module.exports.gamesAddOne = function(req, res) {
    
    Game
    .create({
        teams: req.body.teams,
        startTime: req.body.startTime,
        endTime: req.body.endTime
    }, function(err, game) {
        if (err) {
            console.log('Error creating game');
            res
            .status(400)
            .json(err);
        } else {
            console.log('Game created ', game);
            res
            .status(201)
            .json(game);
        }
    });
    
};

module.exports.gamesUpdateOne = function(req, res) {
    
    var gameId = req.params.gameId;
    console.log("PUT the game id " + gameId);
    
    Game
    .findById(gameId)
    .exec(function(err, doc) {
        
        var response = {
            'status': 200,
            'message': doc
        };
        
        if (err) {
            console.log('Error finding a game');
            response.status = 500;
            response.message = err;
        } else if (!doc) {
            console.log('Game id not found in database: ', id);
            response.status = 404;
            response.message = {
                message: 'Game ID not found ' + gameId
            };
        }
        
        if (response.status != 200) {
            res
            .status(response.status)
            .json(response.message);
        } else {
            // Update returned game document with form data
            var teams = req.body.teams;
            //for (let o of oppnts) {
            for( var i = 0; i < teams.length; i++) {
                let t = teams[i];
                console.log(t)
                if ("score" in t) {
                    console.log('found score')
                    doc.opponents[i].score = parseInt(t.score, 10);
                }
                if ("members" in t) {
                    console.log('found members')
                    doc.opponents[i].members = t.members;
                }
            }
            if ("startTime" in req.body) {
                console.log('found start time')
                doc.startTime = req.body.startTime;
            }
            if ("endTime" in req.body) {
                console.log('found end time')
                doc.endTime = req.body.endTime;
            }
            
            doc.save(function(err, gameUpdated) {
                if (err) {
                    res
                    .status(500)
                    .json(err);
                } else {
                    res
                    .status(200)
                    .json(gameUpdated);
                }
            })
            
        }
    });
};

module.exports.gamesDeleteOne = function(req, res) {
    var gameId = req.params.gameId;
    
    Game
    .findByIdAndRemove(gameId)
    .exec(function(err, game) {
        
        if (err) {
            res
            .status(404)
            .json(err);
        } else {
            res
            .status(204)
            .json();
        }
        
    });
};
