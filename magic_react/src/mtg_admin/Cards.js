import React, {Component} from 'react';
import MagicAPI from './APIClient'
// import $ from "jquery";

class Card extends Component {

    constructor(options) {
        super();
        this.state = {
            name: '',
            age: '',
            image_url: '',
            card_id: options.value,
            height: 120,
            previous_state: {}
        };
    }

    onMouseEnter() {
        this.setState({
            height: null,
            previous_state: this.state
        })
    }

    onMouseLeave() {
        this.setState(this.state.previous_state)
    }

    render() {
        //<img alt='{ this.state.name }' src='{this.state.image_url}'/>
        const img_props = {
            src: this.state.image_url ? 'http://127.0.0.1:8000' + this.state.image_url : null,
            height: this.state.height,
            width: null
        };
        return (<div className='card-img-wrapper'>
            <img alt={this.state.name} {...img_props} className="hover-enlarge" id={this.state.external_id}
                 onMouseEnter={() => this.onMouseEnter()} onMouseLeave={() => this.onMouseLeave()}/>
        </div>)
    }

    componentDidMount() {
        this.loadData().then(data => {
            this.setState(data);
        })
    }

    loadData() {
        return MagicAPI.get('/api/cards/' + this.state.card_id + '/').then(data => data)
    }
}

export default Card;