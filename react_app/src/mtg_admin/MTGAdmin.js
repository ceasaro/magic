import React, {Component} from 'react';
import '../css/MTGAdmin.css';
import '../css/layout/magic.css';
import MagicAPI from './APIClient'
import Deck from './Deck';
import Card from './Cards';
import Mana from './Mana';
import {Sets, SetsFilter} from './Sets'
import {CardTypes, CardTypesFilter} from './CardTypes'
import _ from 'lodash'
import update from 'immutability-helper';

class MTGAdmin extends Component {
    constructor() {
        super();
        this.empty_mana = {w: 0, u: 0, b: 0, r: 0, g: 0,};
        this.state = {
            card_count: 0,
            all_cards: [],
            selected_cards: [],
            filter: {
                sets: [],
                card_types: [],
                q: '',
                mana: this.empty_mana
            },
            show_filter: true,
        }
    }

    mana_count() {
        let count = 0;
        _.forOwn(this.state.filter.mana, function (mana_value, mana) {
            count += mana_value
        });
        return count;
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
            <div key={card.external_id} className="col">
                <Card card={card} height={120} onClick={() => this.handleCardClick(card)}/>
            </div>
        );
        return (
            <div className="container-fluid hidden">
                <div className="row filter-wrapper">
                    <div className="col">
                        <div className="row">
                            <div className="col"><h2>Filter cards <span>({this.state.card_count})</span></h2>
                            </div>
                        </div>
                        <div className="row filtering">
                            <div className="col-4">
                                <div className="form-group">
                                    <label className="filter-label" htmlFor="search_card">Search cards:</label>
                                    <input type="text" className="form-control" id="search_card"
                                           onChange={this.handleSearchChange.bind(this)}/>
                                </div>
                            </div>
                            <div className="col-3">
                                <div className="card-types-filter-wrapper">
                                    <CardTypesFilter onClick={this.selectMTGCardType.bind(this)} selectedTypes={this.state.filter.card_types}/>
                                </div>
                            </div>
                            <div className="col-3">
                                <div className="sets-filter-wrapper">
                                    <SetsFilter onClick={this.selectMTGSet.bind(this)} selectedSets={this.state.filter.sets}/>
                                </div>
                            </div>
                            <div className="col-2">
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
                            </div>
                        </div> {/*row filtering */}


                    </div>
                </div> {/* row filter-wrapper */}

                <div className="row">
                    <div className="col">
                        <div className="row all-cards">
                            {all_cards}
                        </div>
                    </div>
                    <div className="col-2">
                        <h4>Current filter</h4>
                        <div>
                            <b>Mana</b>
                            {this.mana_count() > 0 ?
                                <i className="delete" onClick={this.clearManaFilter.bind(this)}/> : ''}
                            <Mana mana={this.state.filter.mana}/>
                        </div>
                        <div className="seletected-sets-wrapper">
                            <b>Sets</b>
                            {this.state.filter.sets.length > 0 ?
                                <i className="delete" onClick={this.clearSetsFilter.bind(this)}/> : ''}
                            <Sets sets={this.state.filter.sets}/>
                        </div>
                        <div className="seletected-sets-wrapper">
                            <b>CardTypes</b>
                            {this.state.filter.sets.length > 0 ?
                                <i className="delete" onClick={this.clearCardTypesFilter.bind(this)}/> : ''}
                            <CardTypes card_types={this.state.filter.card_types}/>
                        </div>
                    </div>
                </div>
                <div className="row">
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
                <div className="row">
                    <Deck selected_cards={this.state.selected_cards}/>
                </div>

                <div className="row footer">
                    <span>Cees van Wieringen, 2017</span>
                </div>
            </div> // container-fluid
        );
    }

    handleSearchChange(event) {
        let query = event.target.value.length > 2 ? event.target.value : '';
        const new_filter = update(this.state.filter, {
            q: {$set: query},
        });
        this.setState({filter: new_filter});
        this.loadData(new_filter)
    }

    handleManaFilter(event) {
        let mana = event.target.parentElement.getAttribute('data-mana'),
            minus = event.target.getAttribute('class'),
            plus_min = minus.indexOf('mtg-minus') >= 0 ? -1 : 1,
            mana_count = this.state.filter.mana[mana] + plus_min;
        if (mana_count < 0) {
            mana_count = 0;
        }
        if (mana_count >= 20) {
            mana_count = 19;
        }
        const new_filter = update(this.state.filter, {
            mana: {
                [mana]: {$set: mana_count}
            },
        });
        this.setState({filter: new_filter});
        this.loadData(new_filter)
    }

    clearManaFilter() {
        this.setState({
            filter: update(this.state.filter, {
                mana: {$set: this.empty_mana},
            })
        })
    }

    selectMTGSet(event) {
        const set = event.target.value;
        let new_filter;
        if (event.target.checked) {
            new_filter = update(this.state.filter, {sets: {$push: [set]}});
        } else {
            const index = this.state.filter.sets.indexOf(set);
            new_filter = update(this.state.filter, {sets: {$splice: [[index, 1]]}});
        }

        this.setState({filter: new_filter});
        this.loadData(new_filter);
   }

    clearSetsFilter() {
        this.setState({
            filter: update(this.state.filter, {
                sets: {$set: []},
            })
        })
    }

    selectMTGCardType(event) {
        const card_type = event.target.value;
        let new_filter;
        if (event.target.checked) {
            new_filter = update(this.state.filter, {card_types: {$push: [card_type]}});
        } else {
            const index = this.state.filter.card_types.indexOf(card_type);
            new_filter = update(this.state.filter, {card_types: {$splice: [[index, 1]]}});
        }

        this.setState({filter: new_filter});
        this.loadData(new_filter);
    }

    clearCardTypesFilter() {
        this.setState({
            filter: update(this.state.filter, {
                card_types: {$set: []},
            })
        })
    }

    handleCardClick(card) {
        let selected_cards = this.state.selected_cards.splice(0);
        selected_cards.push(card);
        this.setState({selected_cards: selected_cards})
    }

    componentDidMount() {
        this.loadData();
    }

    loadData(opts) {
        let options = _.extend({next: false, previous: false, q: '', mana: this.empty_mana, sets: []}, opts),
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
            _.forEach(options.sets, function (set_name) {
                query_string += 's=' + set_name + '&';
            });
            _.forEach(options.card_types, function (card_type) {
                query_string += 'ct=' + card_type + '&';
            });
        }
        if (query_string) {
            url += '?' + query_string
        }
        return MagicAPI.get(url).then(data => {
            this.setState({
                card_count: data.count,
                next: data.next,
                previous: data.previous,
                all_cards: data.results,
                deck_cards: this.state.deck_cards,
            })
        });
    }
}

export default MTGAdmin;
