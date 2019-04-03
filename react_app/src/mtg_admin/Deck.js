import React, {Component} from 'react';
import MagicAPI from "./APIClient";
import Card from './Cards';
import _ from "lodash";

class Deck extends Component {

    constructor(options) {
        super();
        this.state = {
            new_deck_name: '',
            deck: null,
            found_decks: [],
            selected_cards: options.selected_cards
        };
    }

    componentWillReceiveProps(props) {
        this.setState({selected_cards: props.selected_cards});
    }

    render() {
        const selected_cards = this.state.selected_cards.map((selected_card, index) =>
            <div key={selected_card.external_id + '_' + index} className="col">
                <Card card={selected_card} height={120} onClick={() => this.handleSelectedCardClick(selected_card)}/>
            </div>
        );
        const deck_cards = this.state.deck
            ? this.state.deck.cards.map((deck_card, index) =>
                <div key={deck_card.external_id + '_' + index} className="col">
                    <Card card={deck_card} height={120} onClick={() => this.handleDeckCardClick(deck_card)}/>
                </div>
            )
            : <div>Deck has no cards</div>;
        const button_title = this.state.deck ? "Save " + this.state.deck.name + " deck" : "Create " + this.state.new_deck_name + " deck";
        const found_decks = this.state.found_decks.map((deck) =>
            <li key={deck.name}>
                <button className="btn btn-primary" onClick={() => this.handleSelectDeckClick(deck)}
                        value={deck.name}>{deck.name}</button>
            </li>
        );
        return (
            <div className="new-deck-container">
                <div className="col">
                    <div className="row deck-name">
                        <div className="col">
                            <input type="text" value={this.state.new_deck_name} onChange={this.setDeckName.bind(this)}/>
                        </div>
                        <div className="col">
                            <input type="text" onChange={this.handleSearchDeck.bind(this)}/>
                            Search deck
                        </div>
                        <div className="col">
                            {found_decks}
                        </div>
                    </div>
                    <div className="row selected-cards">
                        {selected_cards}
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
                    cards: _.map(this.state.deck.cards, 'external_id').concat(_.map(this.state.selected_cards, 'external_id'))
                }
            ).then(data => {
                // this.setState({deck: data});
            })
        } else {
            MagicAPI.post('/api/decks/', {
                    name: this.state.new_deck_name,
                    cards: _.map(this.state.deck.cards, 'external_id').concat(_.map(this.state.selected_cards, 'external_id'))
                }
            ).then(data => {
                // this.setState({deck: data});
            })
        }
    }

    handleSearchDeck(event) {
        let query = event.target.value;
        if (query.length > 2) {
            MagicAPI.get('/api/decks/?query=' + query).then(data => {
                this.setState({found_decks: data.results})
            })
        }
    }

    handleSelectDeckClick(clicked_deck) {
        this.setState({deck: clicked_deck, found_decks: []})
    }

    handleDeckCardClick(card) {
        let deck_cards = this.state.deck.cards.splice(0);
        _.remove(deck_cards, function (c) {
            return card.external_id === c.external_id
        });
        this.setState({selected_cards: deck_cards})
    }

    handleSelectedCardClick(card) {
        let selected_cards = this.state.selected_cards.splice(0);
        _.remove(selected_cards, function (c) {
            return card.external_id === c.external_id
        });
        this.setState({selected_cards: selected_cards})
    }

}

export default Deck;