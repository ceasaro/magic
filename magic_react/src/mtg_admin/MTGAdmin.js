import React, {Component} from 'react';
import './MTGAdmin.css';
import MagicAPI from './APIClient'
import Card from './Cards';
import _ from 'lodash'

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
            <div key={card.external_id} className="col"><Card card={card} height={120} onClick={() => this.handleAllCardsClick(card)}/></div>
        );
        const deck_cards = this.state.deck_cards.map((deck_card, index) =>
            <div key={deck_card.external_id + '_' + index} className="col">{deck_card.name}<Card card={deck_card} height={120} onClick={() => this.handleDeckCardsClick(deck_card)}/></div>
        );
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col"><h2>Create a deck</h2>
                    </div>
                </div>
                <div className="row navigation">
                    <div className="col">
                        <div className="form-group">
                            <label htmlFor="usr">Search cards:</label>
                            <input type="text" className="form-control" id="usr" onChange={this.handleSearchChange.bind(this)}/>
                        </div>
                    </div>
                    <div className="col">
                        <button className="btn btn-primary" type="submit"
                                onClick={() => this.loadData({'previous': true})}>
                            Previous
                        </button>
                    </div>
                    <div className="col">
                        <button className="btn btn-primary" type="submit"
                                onClick={() => this.loadData({'next': true})}>
                            Next
                        </button>
                    </div>
                </div>
                <div className="row all-cards">
                    {all_cards}
                </div>
                <div className="row deck-cards">
                    {deck_cards}
                </div>
            </div>
        );
    }

    componentDidMount() {
        this.loadData();
    }

    handleAllCardsClick(card) {
        let deck_cards = this.state.deck_cards.splice(0);
        deck_cards.push(card);
        this.setState({deck_cards: deck_cards})
    }

    handleDeckCardsClick(card) {
        let deck_cards = this.state.deck_cards.splice(0);
        _.remove(deck_cards, function(c) {
            return card.external_id === c.external_id
        });
        this.setState({deck_cards: deck_cards})
    }

    handleSearchChange(event) {
        let query = event.target.value;
        if (query.length > 2) {
            this.loadData({q:query})
        }
    }

    loadData(opts) {
        let options = _.extend({next:false, previous:false, q:null}, opts),
            url = '/api/cards/';
        if (options.next) {
            url = this.state.next
        } else if (options.previous) {
            url = this.state.previous
        } else if (options.q) {
            url += '?q=' + options.q
        }
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
