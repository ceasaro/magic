let _ = require('lodash');

let MagicAPI = {
    'get': function (path, get_options) {
        return this._fetch(path, get_options)
    },
    'post': function (path, post_options) {
        _.extend({method: 'post'}, post_options);
        return this._fetch(path, post_options)
    },
    'put': function (path, put_options) {
        _.extend({method: 'put'}, put_options);
        return this._fetch(path, put_options)
    },
    'remove': function (path, delete_options) {
        _.extend({method: 'delete'}, delete_options);
        return this._fetch(path, delete_options)
    },
    '_fetch': function (path, options) {
        return window
            .fetch(path.startsWith('http')? path: 'http://localhost:8000' + path, options)
            .then(response => response.json())
    },
};


export default MagicAPI;