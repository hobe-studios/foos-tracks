import { gameHistoryConstants } from '../actionTypes';

export function gameHistory(state = {}, action) {
  switch (action.type) {
    case gameHistoryConstants.GETALL_REQUEST:
      return {
        loading: true
      };
    case gameHistoryConstants.GETALL_SUCCESS:
      return {
        items: action.games
      };
    case gameHistoryConstants.GETALL_FAILURE:
      return { 
        error: action.error
      };
    case gameHistoryConstants.DELETE_REQUEST:
      // add 'deleting:true' property to game being deleted
      return {
        ...state,
        items: state.items.map(game =>
          game._id === action.id
            ? { ...game, deleting: true }
            : game
        )
      };
    case gameHistoryConstants.DELETE_SUCCESS:
      // remove deleted game from state
      return {
        items: state.items.filter(game => game._id !== action.id)
      };
    case gameHistoryConstants.DELETE_FAILURE:
      // remove 'deleting:true' property and add 'deleteError:[error]' property to user 
      return {
        ...state,
        items: state.items.map(game => {
          if (game._id === action.id) {
            // make game of user without 'deleting:true' property
            const { deleting, ...gameCopy } = game;
            // return copy of game with 'deleteError:[error]' property
            return { ...gameCopy, deleteError: action.error };
          }
          return game;
        })
      };
    default:
      return state
  }
}