let _ = require('lodash');

let MagicAPI = {
    API_DOMAIN: 'http://127.0.0.1:8000',
    get: function (path, get_options) {
        return this._fetch(path, get_options)
    },
    post: function (path, post_options) {
        _.extend({method: 'post'}, post_options);
        return this._fetch(path, post_options)
    },
    put: function (path, put_options) {
        _.extend({method: 'put'}, put_options);
        return this._fetch(path, put_options)
    },
    remove: function (path, delete_options) {
        _.extend({method: 'delete'}, delete_options);
        return this._fetch(path, delete_options)
    },
    card_img_url: function (card) {
      return card.image_url ? this.API_DOMAIN + card.image_url : null
    },
    _fetch: function (path, options) {
        return window
            .fetch(path.startsWith('http')? path: this.API_DOMAIN + path, options)
            .then(this._handleErrors)
            .then(response => response.json())
    },
    _handleErrors: function(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}
};


export default MagicAPI;