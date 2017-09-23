import React, {Component} from 'react';
import MagicAPI from './APIClient'

class SetsFilter extends Component {

    constructor(options) {
        super();
        this.state = {
            sets: [],
            selectedSets: options.selectedSets,
        }

    }

    render() {
        const all_sets = this.state.sets.map((set, index) =>
            <div key={set.name} className={'mtg-set ' + (this.props.selectedSets.includes(set.name)?'selected':'')}>
                <input type="checkbox" value={set.name} id={'set-' + index + '-' + set.name} onClick={this.props.onClick}/>
                <label htmlFor={'set-' + index + '-' + set.name}>{set.name}</label>
            </div>
        );
        return (
            <div className="sets-filter">{all_sets}</div>
        )
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        let url = '/api/sets/';
        return MagicAPI.get(url)
            .then(data => {
                this.setState({
                    sets: data,
                })
            })
            .catch(error => {
                console.error("Could not get sets from: " + url);
            });
    }
}

export default SetsFilter;