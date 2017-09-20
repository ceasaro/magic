import React, {Component} from 'react';

// import MagicAPI from './APIClient'

class Card extends Component {

    constructor(options) {
        super();
        this.state = {
            card:options.card,
            height: options.height,
            original_height: options.height,
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
        let card = this.state.card,
            same_size = this.state.height === this.state.original_height;
        const img_props = {
            src: card.image_url ? 'http://127.0.0.1:8000' + card.image_url : null,
            height: this.state.height,
            width: null,
            style: {position: same_size?null:'absolute', zIndex: same_size?null:10}
        };
        const card_img_wrapper_style = {height: this.state.original_height, position: 'relative'}
        return (<div className='card-img-wrapper' style={card_img_wrapper_style}>
            <img alt={card.name} {...img_props} className="hover-enlarge" id={card.external_id}
                 onMouseEnter={() => this.onMouseEnter()} onMouseLeave={() => this.onMouseLeave()}/>
        </div>)
    }

    // componentDidMount() {
    //     this.loadData().then(data => {
    //         this.setState(data);
    //     })
    // }
    //
    // loadData() {
    //     return MagicAPI.get('/api/cards/' + this.props.card_id + '/').then(data => data)
    // }
}

export default Card;