import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import MTGGame from './mtg_game/MTGGame';
import registerServiceWorker from './registerServiceWorker';
import MTGAdmin from "./mtg_admin/MTGAdmin";

const compontent = window.location.pathname.startsWith('/admin') ? <MTGAdmin/> : <MTGGame/>;

ReactDOM.render(
    <div className="container-fluid hidden">
        {compontent}
        <div className="row footer">
            <span>Cees van Wieringen, 2017</span>
        </div>
    </div> // container-fluid
    ,
    document.getElementById('mtg_admin')
);
registerServiceWorker();
