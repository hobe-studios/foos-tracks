var express = require('express');
var router = express.Router();

var userCntl = require('../controllers/users.controllers.js')

// User Routes
router
    .route('/')
    .get(userCntl.usersGetAll);

router
    .route('/register')
    .post(userCntl.usersRegister);

router
    .route('/authenticate')
    .post(userCntl.usersAuthenticate);

router
    .route('/:userId')
    .get(userCntl.usersGetOne)
    .put(userCntl.usersUpdateOne)
    .delete(userCntl.usersDeleteOne);

module.exports = router;
