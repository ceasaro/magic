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
        let img_url = MagicAPI.card_img_url(card);
        const img_props = {
            src: img_url,
            height: this.state.height,
            width: null,
            className: same_size ? 'hover-enlarge' : 'large-hovering-img'
        };
        let image_html = []
        if (img_url) {
            image_html.push(<img alt={card.name} {...img_props} id={card.external_id}
                                   onMouseEnter={() => this.onMouseEnter()} onMouseLeave={() => this.onMouseLeave()}
                                   onClick={this.props.onClick}/>)
        } else {
            image_html.push(<span onClick={this.downloadImage.bind(this)}>download</span>)
        }
        return (<div className='card-img-wrapper'>
            {image_html}
        </div>)
    }

    downloadImage() {
        console.log('downloading '+ this.state.card.external_id)
        MagicAPI.put('/api/cards/'+this.state.card.external_id+'/download_img/').then(data => {
            this.setState({card: data})
        })
    }

}

export default Card;