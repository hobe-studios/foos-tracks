var express = require('express');
var router = express.Router();

var gameCntl = require('../controllers/games.controllers.js')

// User Routes
router
    .route('/')
    .get(gameCntl.gamesGetAll)
    .post(gameCntl.gamesAddOne);

router
    .route('/:gameId')
    .get(gameCntl.gamesGetOne)
    .put(gameCntl.gamesUpdateOne)
    .delete(gameCntl.gamesDeleteOne);

module.exports = router;
