import React, {Component} from 'react';
import MagicAPI from './APIClient'


class Card extends Component {

    constructor(options) {
        super();
        this.state = {
            card: options.card,
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
            src: MagicAPI.card_img_url(card),
            height: this.state.height,
            width: null,
            className: same_size? 'hover-enlarge': 'large-hovering-img'
        };
        return (<div className='card-img-wrapper' >
            <img alt={card.name} {...img_props} id={card.external_id}
                 onMouseEnter={() => this.onMouseEnter()} onMouseLeave={() => this.onMouseLeave()} onClick={this.props.onClick}/>
        </div>)
    }

}

export default Card;