var mongoose = require('mongoose');
var dburl = 'mongodb://localhost:27017/foosgenie';

mongoose.connect(dburl);

mongoose.connection.on('connected', function() {
        console.log('Mongoose connected to ' + dburl);
});

mongoose.connection.on('disconnected', function() {
    console.log('Mongoose disconnected from ' + dburl);
});

mongoose.connection.on('error', function(err) {
    console.log('Mongoose connection error: ' + err);
});

process.on('SIGINT', function() {
    mongoose.connection.close(function() {
        console.log('Mongoose disconnected through app termination (SIGINT)')
        process.exit(0);
    });
});

process.on('SIGTERM', function() {
    mongoose.connection.close(function() {
        console.log('Mongoose disconnected through app termination (SIGTERM)')
        process.exit(0);
    });
});

// Capture special signal from nodemon (typing 'rs' in nodemon console)
process.once('SIGUSR2', function() {
    mongoose.connection.close(function() {
        console.log('Mongoose disconnected through app termination (SIGUSR2)')
        process.kill(process.pid, 'SIGUSR2');
    });
});

// Bring in schema and add models
require('./foos.model.js');