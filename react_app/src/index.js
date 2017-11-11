import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import MTGAdmin from './mtg_admin/MTGAdmin';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<MTGAdmin />, document.getElementById('mtg_admin'));
registerServiceWorker();
