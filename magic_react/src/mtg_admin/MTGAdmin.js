import React, {Component} from 'react';
import './MTGAdmin.css';
import Card from './Cards';

class MTGAdmin extends Component {
    render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col"><h2>TODO</h2>
                    </div>
                </div>
                <div className="row hand">
                    <div className="col"></div>
                </div>
                <div className="row">
                    <div className="col"><Card value={'6af5e90daee0c2d5c11d22c64da7dec938b26216'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col"><Card value={'57fce593d9a13f161e674c70a66cb669f0199de1'}/></div>
                    <div className="col">Col3</div>
                </div>
            </div>
        );
    }
}

export default MTGAdmin;
