import React, {Component} from 'react';
import './MTGAdmin.css';
import MagicAPI from './APIClient'
import Card from './Cards';

class MTGAdmin extends Component {
    constructor() {
        super();
        this.state = {
            all_cards: [],
            deck_cards: [],
        }
    }

    render() {
        const all_cards = this.state.all_cards.map((card) =>
            <div key={card.external_id} className="col"><Card card={card} height={120}/></div>
        );
        const deck_cards = this.state.deck_cards.map((card) =>
            <div key={card.external_id} className="col"><Card card={card} height={120}/></div>
        );
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col"><h2>Create a deck</h2>
                    </div>
                </div>
                <div className="row navigation">
                    <div className="col"><button className="btn btn-primary" type="submit" onClick={() => this.loadData('previous')}>Previous</button></div>
                    <div className="col"><button className="btn btn-primary" type="submit" onClick={() => this.loadData('next')}>Next</button></div>
                </div>
                <div className="row all-cards">
                    {all_cards}
                </div>
                <div className="row all-cards">
                    {deck_cards}
                </div>
            </div>
        );
    }

    componentDidMount() {
        this.loadData();
    }

    loadData(option) {
        let url = '/api/cards/';
        if (option === 'next') {
            url = this.state.next
        } else if (option === 'previous') {
            url = this.state.previous
        }
        console.log(url);
        return MagicAPI.get(url).then(data => {
            this.setState({
                next: data.next,
                previous: data.previous,
                all_cards: data.results,
                deck_cards: this.state.deck_cards,
            })
        });
    }
}

export default MTGAdmin;
