var mongoose = require('mongoose');
var bcrypt = require('bcrypt');

var userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    nfcId: String,
    password: String
});

// https://stackoverflow.com/questions/43092071/how-should-i-store-salts-and-passwords-in-mongodb
// hash the password
userSchema.statics.generateHash = function(password) {
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

// checking if password is valid
userSchema.statics.validPassword = function(password) {
    return bcrypt.compareSync(password, this.password);
}

var teamSchema = new mongoose.Schema({
    members: [String],
    name: String
})

var gameSchema = new mongoose.Schema({
    datePlayed: {
        type: Date,
        "default": Date.now
    },
    teams: [teamSchema],
    scores: [Number],
    startTime: {
        type: Date,
        "default": Date.now
    },
    endTime: Date
});

mongoose.model('User', userSchema);
mongoose.model('Game', gameSchema);