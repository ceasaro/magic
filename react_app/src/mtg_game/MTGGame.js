import React, {Component} from 'react';
import '../css/MTGAdmin.css';
import '../css/layout/magic.css';

class MTGGame extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <div id="MTGGame">

                <div className="row filter-wrapper">
                    <div className="col">
                        <div className="row">
                            <div className="col"><h2>Game</h2>
                            </div>
                        </div>
                    </div>
                </div>
            </div> // MTGGame
        );
    }
}

export default MTGGame;
