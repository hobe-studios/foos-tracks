import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { gameHistoryActions } from '../../actions';

class GameHistoryPage extends React.Component {
    componentDidMount() {
        this.props.getPastGames();
    }

    handleDeleteGame(id) {
        return (e) => this.props.deleteGame(id);
    }

    render() {
        const { gameHistory } = this.props;
        return (
            <div className="col-md-6 col-md-offset-3">
                <h1>Games Played</h1>
                {gameHistory.loading && <em>Loading games played ...</em>}
                {gameHistory.error && <span className="text-danger">ERROR: {gameHistory.error}</span>}
                {gameHistory.items &&
                    <ul>
                        {gameHistory.items.map((game, index) =>
                            <li key={game._id}>
                                {'Start: ' + game.startTime + ', End: ' + game.endTime}
                                {
                                    game.deleting ? <em> - Deleting...</em>
                                    : game.deleteError ? <span className="text-danger"> - ERROR: {game.deleteError}</span>
                                    : <span> - <a onClick={this.handleDeleteGame(game._id)}>Delete</a></span>
                                }
                            </li>
                        )}
                    </ul>
                }
                <p>
                    <Link to="/login">Logout</Link>
                </p>
            </div>
        );
    }
}

function mapStateToProps(state) {
    const { gameHistory } = state;
    return {
        gameHistory
    };
}

function mapDispatchToProps(dispatch) {
    return {
        getPastGames: () => dispatch(gameHistoryActions.getAll()),
        getPastGame: (id) => dispatch(gameHistoryActions.getOne(id)),
        deleteGame: (id) => dispatch(gameHistoryActions.delete(id))
    };
}

const connectedGameHistoryPage = connect(mapStateToProps, mapDispatchToProps)(GameHistoryPage);
export {connectedGameHistoryPage as GameHistoryPage}