var mongoose = require('mongoose');
var User = mongoose.model('User');

module.exports.usersGetAll = function(req, res) {
    
    var offset = 0;
    var count = 5;
    var maxCount = 10;
    
    if (req.query && req.query.lat && req.query.long) {
        runGeoQuery(req, res);
        return;
    }
    
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
    
    User
    .find()
    .skip(offset)
    .limit(count)
    .exec(function(err, users) {
        if (err) {
            console.log('Error finding users');
            res
            .status(500)
            .json(err);
        } else {
            console.log('Found users', users.length);
            res
            .status(200)
            .json(users);
        }
    });
    
};

module.exports.usersGetOne = function(req, res) {
    
    var userId = req.params.userId;
    console.log("GET the user id " + userId);
    
    User
    .findById(userId)
    .exec(function(err, doc) {
        
        var response = {
            'status': 200,
            'message': doc
        };
        
        if (err) {
            console.log('Error finding a user');
            response.status = 500;
            response.message = err;
        } else if (!doc) {
            console.log('User id not found in database: ', userId);
            response.status = 404;
            response.message = {
                message: 'User ID not found ' + userId
            };
        }
        
        res
        .status(response.status)
        .json(response.message);
        
    });
};

module.exports.usersRegister = function(req, res) {
    
    var userName = req.body.userName;
    var password = req.body.password;
    var firstName = req.body.firstName;
    var lastName = req.body.lastName;

    // TODO: Validate the password is secure enough

    // TODO: Ensure that username is not already taken
    User
    .find({userName: userName})
    .exec(function(err, doc) {
        
        if (err) {
            console.log('Error when trying to find if user already exists in db');
            res
            .status(500)
            .json(err);
            return
        } else if (doc.length > 0) { 
            console.log('Username already exists, cannot register with this name.');
            res.status(400);
            res.json({
                message: 'Username already exists in database: ' + userName
            });
            return
        }

        // Create user
        User
        .create({
            userName: userName,
            firstName: firstName,
            lastName: lastName,
            password: User.generateHash(password),
            nfcId: makeId()
        }, function(err, user) {
            if (err) {
                console.log('Error creating user');
                res
                .status(400)
                .json(err);
            } else {
                console.log('User created ', user);
                res
                .status(201)
                .json(user);
            }
        });
    });
};

module.exports.usersAuthenticate = function(req, res) {

    var userName = req.body.userName;
    var password = req.body.password;

    // Find user in database
    User
    .find({ userName: userName})
    .exec(function(err, doc) {
        var response = {
            'status': 500,
            'message': {
                message: "Unknown error occurred"
            }
        };
        
        if (err) {
            console.log('Error finding a user');
            res.status(500);
            res.json(err);
            return;
        } else if (doc.length == 0) {
            console.log('User id not found in database: ', userName);
            res.status(500);
            res.json({
                message: 'Authentication failed'
            });
            return;
        }
        
        let user = doc[0]
        if (user.validatePassword(password)) {
            response.status = 200
            response.message = user
        } else {
            console.log('Invalid password provided');
            response.status = 401
            response.message = {
                message: 'Authentication failed'
            };
        }

        res
        .status(response.status)
        .json(response.message);
    })

}

module.exports.usersUpdateOne = function(req, res) {
    
    var userId = req.params.userId;
    console.log("GET the user id " + userId);
    
    User
    .findById(userId)
    .exec(function(err, doc) {
        
        var response = {
            'status': 200,
            'message': doc
        };
        
        if (err) {
            console.log('Error finding a user');
            response.status = 500;
            response.message = err;
        } else if (!doc) {
            console.log('User id not found in database: ', id);
            response.status = 404;
            response.message = {
                message: 'User ID not found ' + userId
            };
        }
        
        if (response.status != 200) {
            res
            .status(response.status)
            .json(response.message);
        } else {
            // Update returned user document with form data
            doc.name = req.body.name;
            doc.nfcId = req.body.nfcId;
            
            doc.save(function(err, userUpdated) {
                if (err) {
                    res
                    .status(500)
                    .json(err);
                } else {
                    res
                    .status(204)
                    .json();
                }
            })
            
        }
    });
};

module.exports.usersDeleteOne = function(req, res) {
    var userId = req.params.userId;
    
    User
    .findByIdAndRemove(userId)
    .exec(function(err, user) {
        
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

// https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
var makeId = function() {
    var length = 5;
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    
    for (var i = 0; i < length; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));
    
    return text;
}

var runGeoQuery = function(req, res) {
    
    var lat = parseFloat(req.query.lat);
    var long = parseFloat(req.query.long);
    
    // Validate query params
    if (isNaN(lat) || isNaN(long)) {
        res
        .status(400)
        .json({
            "message": "If supplied in query string, lat and long should be floats."
        });
        return;
    }
    
    // geoJSON point
    var point = {
        type: "Point",
        coordinates: [long, lat]
    };
    
    var geoOptions = {
        spherical: true,
        maxDistance: 2000,
        num: 5
    };
    
    User
    .geoNear(point, geoOptions, function(err, results, stats) {
        console.log('Geo results', results);
        console.log('Geo stats', stats);
        if (err) {
            console.log('Error finding users using geo location')
            res
            .status(500)
            .json(err);
        } else {
            res
            .status(200)
            .json(results);
        }
    });
    
};

var _splitArray = function(input) {
    var output;
    if (input && input.length > 0) {
        output = input.split(';');
    } else {
        output = [];
    }
    return output;
};