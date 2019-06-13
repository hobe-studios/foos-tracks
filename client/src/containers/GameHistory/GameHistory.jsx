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
            <div className="">
                <h1>Games Played</h1>
                {gameHistory.loading && <em>Loading games played ...</em>}
                {gameHistory.error && <span className="text-danger">ERROR: {gameHistory.error}</span>}
                {gameHistory.items &&

                    <table className="table table">
                        <th>
                            <td>Team 1</td>
                            <td>Team 2</td>
                            <td>Score</td>
                            <td>Start Time</td>
                            <td>End Time</td>
                        </th>
                        {gameHistory.items.map((game, index) => {
                            let team1 = game.teams[0]
                            let team2 = game.teams[1]
                            return <tr>
                                <td>team1.name</td>
                                <td>team2.name</td>
                                <td>{team1.score + ' - ' + team2.score}</td>
                                <td>{game.startTime}</td>
                                <td>{game.endTime}</td>
                            </tr>
                        })}
                    </table>
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