import React, {Component} from 'react';
import '../css/MTGAdmin.css';
import '../css/layout/magic.css';
import MagicAPI from './APIClient'
import Card from './Cards';
import Mana from './Mana';
import _ from 'lodash'
import update from 'immutability-helper';

class MTGAdmin extends Component {
    constructor() {
        super();
        this.state = {
            all_cards: [],
            deck_cards: [],
            filter: {
                q: '',
                mana: {w: 0, u: 0, b: 0, r: 0, g: 0,}
            }
        }
    }

    render() {
        const next_button_attrs = {};
        if (!this.state.next) {
            next_button_attrs['disabled'] = 'disabled'
        }
        const previous_button_attrs = {};
        if (!this.state.previous) {
            previous_button_attrs['disabled'] = 'disabled'
        }
        const all_cards = this.state.all_cards.map((card) =>
            <div key={card.external_id} className="col"><Card card={card} height={120}
                                                              onClick={() => this.handleAllCardsClick(card)}/></div>
        );
        const deck_cards = this.state.deck_cards.map((deck_card, index) =>
            <div key={deck_card.external_id + '_' + index} className="col">{deck_card.name}<Card card={deck_card}
                                                                                                 height={120}
                                                                                                 onClick={() => this.handleDeckCardsClick(deck_card)}/>
            </div>
        );
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col"><h2>Create a deck</h2>
                    </div>
                </div>
                <div className="row filtering">
                    <div className="col-3">
                        <div className="form-group">
                            <label className="filter-label" htmlFor="search_card">Search cards:</label>
                            <input type="text" className="form-control" id="search_card"
                                   onChange={this.handleSearchChange.bind(this)}/>
                        </div>
                    </div>
                    <div className="col-3">
                        <label className="filter-label">Mana</label>
                        <div className="mana-filter-selectors">
                            <div className="mana-filter-selector" data-mana="w">
                                <i className="mana-big w" onClick={this.handleManaFilter.bind(this)}/>
                                <i className="mtg-minus" onClick={this.handleManaFilter.bind(this)}/>
                            </div>
                            <div className="mana-filter-selector" data-mana="u">
                                <i className="mana-big blue" onClick={this.handleManaFilter.bind(this)}/>
                                <i className="mtg-minus" onClick={this.handleManaFilter.bind(this)}/>
                            </div>
                            <div className="mana-filter-selector" data-mana="b">
                                <i className="mana-big black" onClick={this.handleManaFilter.bind(this)}/>
                                <i className="mtg-minus" onClick={this.handleManaFilter.bind(this)}/>
                            </div>
                            <div className="mana-filter-selector" data-mana="r">
                                <i className="mana-big red" onClick={this.handleManaFilter.bind(this)}/>
                                <i className="mtg-minus" onClick={this.handleManaFilter.bind(this)}/>
                            </div>
                            <div className="mana-filter-selector" data-mana="g">
                                <i className="mana-big green" onClick={this.handleManaFilter.bind(this)}/>
                                <i className="mtg-minus" onClick={this.handleManaFilter.bind(this)}/>
                            </div>
                        </div>
                        <Mana mana={this.state.filter.mana}/>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        <div className="row all-cards">
                            {all_cards}
                        </div>
                        <div className="row deck-cards">
                            {deck_cards}
                        </div>
                    </div>
                    <div className="col-2">
                    </div>
                </div>
                <div className="row footer">
                    <div className="col">
                        <button className="btn btn-primary" type="submit" {...previous_button_attrs}
                                onClick={() => this.loadData({'previous': true})}>
                            Previous
                        </button>
                    </div>
                    <div className="col">
                        <button className="btn btn-primary" type="submit" {...next_button_attrs}
                                onClick={() => this.loadData({'next': true})}>
                            Next
                        </button>
                    </div>
                </div>
            </div> // container-fluid
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
        _.remove(deck_cards, function (c) {
            return card.external_id === c.external_id
        });
        this.setState({deck_cards: deck_cards})
    }

    handleManaFilter(event) {
        let mana = event.target.parentElement.getAttribute('data-mana'),
            minus = event.target.getAttribute('class'),
            plus_min = minus.indexOf('mtg-minus') >= 0 ? -1 : 1,
            mana_count = this.state.filter.mana[mana] + plus_min;
        if (mana_count < 0) {
            mana_count = 0;
        }
        const new_filter = update(this.state.filter, {
            mana: {
                [mana]: {$set: mana_count}
            },
        });
        this.setState({filter: new_filter});
        this.loadData(new_filter)
    }

    handleSearchChange(event) {
        let query = event.target.value.length > 2 ? event.target.value : '';
        const new_filter = update(this.state.filter, {
            q: {$set: query},
        });
        this.setState({filter: new_filter});
        this.loadData(new_filter)
    }

    loadData(opts) {
        let options = _.extend({next: false, previous: false, q: '', mana: {w: 0, u: 0, b: 0, r: 0, g: 0,}}, opts),
            url = '/api/cards/',
            query_string = '';
        if (options.next) {
            url = this.state.next
        } else if (options.previous) {
            url = this.state.previous
        } else {
            query_string += 'q=' + (options.q ? options.q : '') + '&';  // search query
            query_string += 'a=' + (options.mana.a ? options.mana.a : '') + '&';  // any mana
            query_string += 'w=' + (options.mana.w ? options.mana.w : '') + '&';  // white mana
            query_string += 'u=' + (options.mana.u ? options.mana.u : '') + '&';  // blue mana
            query_string += 'b=' + (options.mana.b ? options.mana.b : '') + '&';  // black mana
            query_string += 'r=' + (options.mana.r ? options.mana.r : '') + '&';  // red mana
            query_string += 'g=' + (options.mana.g ? options.mana.g : '') + '&';  // green mana
            query_string += 'c=' + (options.mana.c ? options.mana.c : '') + '&';  // colorless mana
        }
        if (query_string) {
            url += '?' + query_string
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
