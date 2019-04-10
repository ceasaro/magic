import React, {Component} from 'react';
import MagicAPI from '../apis/APIClient'

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
            <div key={'set-filter-'+set.name} className={'mtg-set ' + (this.props.selectedSets.includes(set.name)?'selected':'')}>
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

function Sets(props) {
    const all_sets = props.sets.map((set_name, index) =>
        <div key={set_name} className='mtg-set'>{set_name}</div>
    );
    return (
        <div className="mtg-sets">{all_sets}</div>
    )
}

export {SetsFilter, Sets};
