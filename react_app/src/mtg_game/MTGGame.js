import React, {Component} from 'react';
import Login from '../auth/Login'
import Game from './Game'
import '../css/MTGGame.css';
import '../css/layout/magic.css';

class MTGGame extends Component {
    constructor() {
        super();
        this.state = {
            player: null
        }
    }

    render() {
        const component = this.state.player ? <Game/> : <Login/>;
        return (
            <div id="MTGGame">
                <div className="row">
                    <div className="col">
                        {component}
                    </div>
                </div>
            </div> // MTGGame
        );
    }
}

export default MTGGame;
