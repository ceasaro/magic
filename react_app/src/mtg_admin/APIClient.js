let _ = require('lodash');

let MagicAPI = {
    API_DOMAIN: 'http://magic.local:8000',
    get: function (path, get_options) {
        return this._fetch(path, get_options)
    },
    post: function (path, data = {}, post_options = {}) {
        _.assignIn(post_options, {
            method: 'post',
            mode: "cors", // no-cors, cors, *same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
                "Content-Type": "application/json",
                // "Content-Type": "application/x-www-form-urlencoded",
            },
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        });
        return this._fetch(path, post_options)
    },
    put: function (path, put_options) {
        _.assignIn(put_options, {method: 'put'});
        return this._fetch(path, put_options)
    },
    remove: function (path, delete_options) {
        _.assignIn(delete_options, {method: 'delete'});
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