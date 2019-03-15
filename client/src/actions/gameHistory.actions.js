import { gameService } from '../services';
import { alertActions } from '.';
import { gameHistoryConstants } from '../actionTypes'

export const gameHistoryActions = {
    getAll,
    getOne,
    delete: _delete
};

function getAll() {
    return dispatch => {
        dispatch(request());

        gameService.getAll()
            .then(
                games => dispatch(success(games)),
                error => dispatch(failure(error.toString()))
            );
    };

    function request() { return { type: gameHistoryConstants.GETALL_REQUEST } }
    function success(games) { return { type: gameHistoryConstants.GETALL_SUCCESS, games } }
    function failure(error) { return { type: gameHistoryConstants.GETALL_FAILURE, error } }
}

function getOne(id) {
    return dispatch => {
        dispatch(request());

        gameService.getOne(id)
            .then(
                game => dispatch(success(game)),
                error => dispatch(failure(error.toString()))
            );
    };

    function request() { return { type: gameHistoryConstants.GETALL_REQUEST } }
    function success(game) { return { type: gameHistoryConstants.GETALL_SUCCESS, game } }
    function failure(error) { return { type: gameHistoryConstants.GETALL_FAILURE, error } }
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    return dispatch => {
        dispatch(request(id));

        gameService.delete(id)
            .then(
                id => dispatch(success(id)),
                error => dispatch(failure(id, error.toString()))
            );
    };

    function request(id) { return { type: gameHistoryConstants.DELETE_REQUEST, id } }
    function success(id) { return { type: gameHistoryConstants.DELETE_SUCCESS, id } }
    function failure(id, error) { return { type: gameHistoryConstants.DELETE_FAILURE, id, error } }
}