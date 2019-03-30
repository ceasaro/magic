import React, {Component} from 'react';
import MagicAPI from "./APIClient";
import Card from './Cards';
import _ from "lodash";

class Deck extends Component {

    constructor(options) {
        super();
        this.state = {
            deck_name: 'Starter player A',
            deck_cards: [],
            selected_cards: options.selected_cards
        };
    }

    componentWillReceiveProps(props) {
        this.setState({selected_cards: props.selected_cards});
    }

    render() {
        console.log("Deck.js");
        console.log(this.state.selected_cards);
        const selected_cards = this.state.selected_cards.map((selected_card, index) =>
            <div key={selected_card.external_id + '_' + index} className="col">
                <Card card={selected_card} height={120} onClick={() => this.handleSelectedCardClick(selected_card)}/>
            </div>
        );
        const deck_cards = this.state.deck_cards.map((deck_card, index) =>
            <div key={deck_card.external_id + '_' + index} className="col">
                <Card card={deck_card} height={120} onClick={() => this.handleDeckCardClick(deck_card)}/>
            </div>
        );
        return (
            <div className="new-deck-container">
                <div className="col">
                    <div className="row deck-name">
                        <input type="text" value={this.state.deck_name} onChange={this.setDeckName.bind(this)}/>
                        <span>{this.state.deck_name}</span>
                    </div>
                    <div className="row selected-cards">
                        {selected_cards}
                    </div>
                    <div className="row deck-cards">
                        {deck_cards}
                    </div>
                    <div className="row">
                        <button className="btn btn-primary" type="submit" onClick={this.saveDeck.bind(this)}>Save deck
                        </button>
                    </div>
                </div>
            </div>

        )
    }

    setDeckName(event) {
        this.setState({deck_name: event.target.value})
    }
    saveDeck() {
        MagicAPI.post('/api/decks/', {
                name: this.state.deck_name,
                cards: _.map(this.state.deck_cards, 'external_id')
            }
        ).then(data => {
        })
    }

    handleDeckCardClick(card) {
        let deck_cards = this.state.deck_cards.splice(0);
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