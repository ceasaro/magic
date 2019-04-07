import React, {Component} from 'react';
import MagicAPI from "./APIClient";
import Card from './Cards';
import _ from "lodash";
import update from 'immutability-helper';

class Deck extends Component {

    constructor(options) {
        super();
        this.state = {
            new_deck_name: '',
            deck: null,
            found_decks: [],
            selected_card: options.selected_card
        };
        this.searchDeck('')
    }

    componentWillReceiveProps(props) {
        let selected_card = props.processSelectedCard();
        if (this.state.deck && selected_card) {
            let deck_cards = this.state.deck.cards.splice(0);
            deck_cards.push(selected_card);
            const new_deck = update(this.state.deck, {
                cards: {$set: deck_cards},
            });
            this.setState({
                deck: new_deck,
            })
        }
    }

    render() {
        const deck_cards = this.state.deck
            ? this.state.deck.cards.map((deck_card, index) =>
                <div className="col" key={deck_card.external_id + '_' + index}>
                    <Card card={deck_card} height={120} onClick={() => this.handleDeckCardClick(deck_card)}/>
                </div>
            )
            : <div>Deck has no cards</div>;
        const button_title = this.state.deck ? "Save " + this.state.deck.name + " deck" : "Create " + this.state.new_deck_name + " deck";
        const found_deck_items = this.state.found_decks.map((deck) =>
            <li key={deck.name} className="list-group-item">
                <button className="btn btn-primary" onClick={() => this.handleSelectDeckClick(deck)}
                        value={deck.name}>{deck.name}</button>
            </li>
        );
        return (
            <div className="row new-deck-container">
                <div className="col ">
                    <div className="row">
                        <div className="col">
                            <h3>{this.state.deck ? this.state.deck.name + "(" + this.state.deck.cards.length + "cards)" : ''} </h3>
                        </div>
                    </div>
                    <div className="row deck-cards">
                        {deck_cards}
                    </div>
                    <div className="row">
                        <div className="col">
                            <button disabled={!this.state.deck && !this.state.new_deck_name} className="btn btn-primary"
                                    type="submit" onClick={this.saveDeck.bind(this)}>{button_title}
                            </button>
                        </div>
                    </div>
                </div>
                <div className="col-2">
                    <div>
                        <input type="text" value={this.state.new_deck_name} onChange={this.setDeckName.bind(this)}
                               placeholder="new deck name"/>
                    </div>
                    <div>
                        <input type="text" onChange={this.handleSearchDeck.bind(this)} placeholder="search deck"/>
                    </div>
                    <div>
                        <ul className="list-group">{found_deck_items}</ul>
                    </div>
                </div>
            </div>

        )
    }

    setDeckName(event) {
        this.setState({new_deck_name: event.target.value})
    }

    saveDeck() {
        if (this.state.deck) {
            MagicAPI.put('/api/decks/' + this.state.deck.name + '/', {
                    name: this.state.new_deck_name || this.state.deck.name,
                    cards: _.map(this.state.deck.cards, 'external_id')
                }
            ).then(data => {
                // this.setState({deck: data});
            })
        } else {
            MagicAPI.post('/api/decks/', {
                    name: this.state.new_deck_name,
                    cards: _.map(this.state.deck.cards, 'external_id')
                }
            ).then(data => {
                // this.setState({deck: data});
            })
        }
    }

    handleSearchDeck(event) {
        let query = event.target.value;
        if (query.length > 1) {
            this.searchDeck(query);
        }
    }

    searchDeck(query) {
        MagicAPI.get('/api/decks/?query=' + query).then(data => {
            this.setState({found_decks: data.results})
        })
    }

    handleSelectDeckClick(clicked_deck) {
        this.setState({deck: clicked_deck, found_decks: []})
    }

    handleDeckCardClick(card) {
        let deck_cards = this.state.deck.cards.splice(0),
            first_index=deck_cards.indexOf(card);
        if (first_index > -1) {
            deck_cards.splice(first_index, 1);
        }
        const new_deck = update(this.state.deck, {
            cards: {$set: deck_cards},
        });
        this.setState({deck: new_deck})
    }

}

export default Deck;