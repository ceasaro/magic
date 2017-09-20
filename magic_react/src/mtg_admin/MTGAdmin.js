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
                <div className="row all-cards">
                    {deck_cards}
                </div>
            </div>
        );
    }

    componentDidMount() {
        this.loadData();
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
