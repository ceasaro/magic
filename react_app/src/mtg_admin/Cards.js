import React, {Component} from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import MagicAPI from './APIClient'


class Card extends Component {

    constructor(options) {
        super();
        this.state = {
            card: options.card,
            height: options.height,
            found_img_hover_index: null,
            found_img_height: options.height,
            img_class_name: 'hover-enlarge',
            original_height: options.height,
            previous_state: {},
            loading: false,
            error_fetching_img: false,
            show_found_cards: false
        };
    }

    onMouseEnter(found_img_index) {
        if (found_img_index >= 0) {
            this.setState({
                found_img_height: '400px',
                found_img_hover_index: found_img_index,
                found_img_class_name: 'large-hovering-img',
                previous_state: this.state
            })
        } else {
            this.setState({
                height: '400px',
                img_class_name: 'large-hovering-img',
                previous_state: this.state
            })
        }
    }

    onMouseLeave() {
        this.setState(this.state.previous_state);
        this.setState({
            found_img_hover_index: null
        })
    }

    foundImgClick(img_url) {
        this.setState({loading: true});
        MagicAPI.patch('/api/cards/' + this.state.card.external_id + '/', {'image_url': img_url})
            .then(data => {
                this.setState({
                    card: data,
                    loading: false,
                    show_found_cards: false
                })
            })
            .catch(error => {
                this.setState({
                    loading: false,
                    error_fetching_img: true,
                    show_found_cards: false
                })
            });
    }

    handleCloseFoundCards() {
        this.setState({show_found_cards: false});
    }

    render() {
        let card = this.state.card;
        let img_url = MagicAPI.card_img_url(card);
        let found_cards = [];
        if (this.state.card.found_img_urls) {
            this.state.card.found_img_urls.map((img_url, index) => found_cards.push(
                <div className='found-img-wrapper col'>
                    <img key={card.external_id + '_' + index}
                         alt={card.name + '_' + index}
                         src={img_url}
                         height={this.state.found_img_hover_index===index?this.state.found_img_height: this.state.height}
                         id={card.external_id + '_' + index}
                         onMouseEnter={() => this.onMouseEnter(index)}
                         onMouseLeave={() => this.onMouseLeave()}
                         onClick={() => this.foundImgClick(img_url)}
                         className={this.state.found_img_hover_index===index?this.state.found_img_class_name: this.state.img_class_name}
                    />
                </div>
            ))
        }

        let image_html = [];
        if (img_url) {
            image_html.push(<img key={card.external_id}
                                 alt={card.name}
                                 src={img_url}
                                 height={this.state.height}
                                 width={null}
                                 className={this.state.img_class_name}
                                 id={card.external_id}
                                 onMouseEnter={() => this.onMouseEnter()}
                                 onMouseLeave={() => this.onMouseLeave()}
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
        return (<div>
            <div className='card-img-wrapper'>
                <div className='card-name'>{this.state.card.name}</div>
                {image_html}
            </div>
                <Modal show={this.state.show_found_cards} onHide={this.handleCloseFoundCards.bind(this)} size="lg">
                    <Modal.Header closeButton>
                        <Modal.Title>Select image for {this.state.card.name}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="row">{found_cards}</div></Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleCloseFoundCards.bind(this)}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
            </div>
        )
    }

    downloadImage() {
        this.setState({loading: true});
        MagicAPI.get('/api/cards/' + this.state.card.external_id + '/download_img/')
            .then(data => {
                this.setState({
                    card: data,
                    loading: false,
                    show_found_cards: Boolean(data.found_img_urls && data.found_img_urls.length)
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