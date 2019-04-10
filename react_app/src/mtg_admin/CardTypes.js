import React, {Component} from 'react';
import MagicAPI from '../apis/APIClient'

class CardTypesFilter extends Component {

    constructor(options) {
        super();
        this.state = {
            types: [],
            selectedTypes: options.selectedTypes,
        }

    }

    render() {
        const all_types = this.state.types.map((card_type, index) =>
            <div key={'card-type-filter-'+card_type} className={'mtg-card-type ' + (this.props.selectedTypes.includes(card_type)?'selected':'')}>
                <input type="checkbox" value={card_type} id={'card-type-' + index + '-' + card_type} onClick={this.props.onClick}/>
                <label htmlFor={'card-type-' + index + '-' + card_type}>{card_type}</label>
            </div>
        );
        return (
            <div className="card-types-filter">{all_types}</div>
        )
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        let url = '/api/card_types/';
        return MagicAPI.get(url)
            .then(data => {
                this.setState({
                    types: data,
                })
            })
            .catch(error => {
                console.error("Could not get types from: " + url);
            });
    }
}

function CardTypes(props) {
    const all_types = props.card_types.map((card_type, index) =>
        <div key={card_type} className='mtg-set'>{card_type}</div>
    );
    return (
        <div className="mtg-sets">{all_types}</div>
    )
}

export {CardTypesFilter, CardTypes};
