var mongoose = require('mongoose');
var bcrypt = require('bcrypt');

var userSchema = new mongoose.Schema({
    userName: {
        type: String,
        required: true
    },
    firstName: {
        type: String,
        required: true
    },
    lastName: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    nfcId: String
});

// https://stackoverflow.com/questions/43092071/how-should-i-store-salts-and-passwords-in-mongodb
// hash the password
userSchema.statics.generateHash = function(password) {
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

// check if password is valid
userSchema.methods.validatePassword = function(password) {
    return bcrypt.compareSync(password, this.password);
}

// var teamSchema = new mongoose.Schema({
//     members: [String],
//     name: String
// })

var gameSchema = new mongoose.Schema({
    teams: [{members: [String], score: Number}],
    startTime: Date,
    endTime: Date
});

mongoose.model('User', userSchema);
mongoose.model('Game', gameSchema);