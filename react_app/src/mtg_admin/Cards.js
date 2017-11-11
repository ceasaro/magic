import React, {Component} from 'react';
import MagicAPI from './APIClient'


class Card extends Component {

    constructor(options) {
        super();
        this.state = {
            card: options.card,
            height: options.height,
            original_height: options.height,
            previous_state: {},
            loading: false,
            error_fetching_img: false,
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
        let image_html = [];
        if (img_url) {
            image_html.push(<img key={card.external_id} alt={card.name} {...img_props} id={card.external_id}
                                 onMouseEnter={() => this.onMouseEnter()} onMouseLeave={() => this.onMouseLeave()}
                                 onClick={this.props.onClick}/>)
        } else if (this.state.loading) {
            image_html.push(<div key="card-loader" className="loader">Loading...</div>)
        } else if (this.state.error_fetching_img) {
            image_html.push(<div key="card-download-error" className="error">Could not download image of {this.state.card.name}</div>)
        } else {
            image_html.push(
                <div key="card-download-button">
                    <button className="btn btn-primary" type="submit" onClick={this.downloadImage.bind(this)}>Download
                    </button>
                </div>)
        }
        return (<div className='card-img-wrapper'>
            <div className='card-name'>{this.state.card.name}</div>
            {image_html}
        </div>)
    }

    downloadImage() {
        this.setState({loading: true});
        MagicAPI.put('/api/cards/' + this.state.card.external_id + '/download_img/')
            .then(data => {
                this.setState({
                    card: data,
                    loading: false
                })
            })
            .catch(error => {
                this.setState({
                    loading: false,
                    error_fetching_img: true
                })
            })
    }
}

export default Card;