/* JS */

define([
    'jquery',
    'backbone',
    'cookie'

], function ($, Backbone) {
    'use strict';

    /**
     * Underscore plugin : analog compact for arrays
     */
    _.mixin({
        compactObject : function(o) {
            _.each(o, function(v, k){
                if(!v)
                    delete o[k];
            });
            return o;
        }
    });


    var urldecode = function(str) {
        return decodeURIComponent((str + '').replace(/%(?![\da-f]{2})/gi, function () {
            // PHP tolerates poorly formed escape sequences
            return '%25';
        }).replace(/\+/g, '%20'));
    };


    var parseQueryString = function( queryString ) {
        var params = {}, queries, temp, i, l;

        // Split into key/value pairs
        queryString = urldecode(queryString);
        queries = queryString.split("&");

        // Convert the array of strings into an object
        for ( i = 0, l = queries.length; i < l; i++ ) {
            temp = queries[i].split('=');
            params[temp[0]] = temp[1];
        }

        return params;
    };


    var setFilter = function(key, val, multi) {
        multi = multi || false;
        var filter = Backbone.history.fragment;
        var filter_obj = parseQueryString( filter );

        if( multi ) {
            if(filter_obj[key] === undefined) {
                filter_obj[key] = val;
            } else {

                var vals = filter_obj[key].toString().split('-');
                vals.push(val.toString());
                filter_obj[key] = _.uniq(vals).join('-');
                //console.log(vals);

            }
        } else {
            filter_obj[key] = val;
        }

        var new_filter = $.param( _.compactObject( filter_obj ) );

        return new_filter;
    };

    var unsetFilter = function(key, val, multi) {
        multi = multi || false;
        var filter = Backbone.history.fragment;
        var filter_obj = parseQueryString( filter );

        if( multi ) {
            if(filter_obj[key] !== undefined) {
                var vals = filter_obj[key].toString().split('-');

                if( vals.length == 1 ) {
                    delete filter_obj[key];
                } else if( vals.length > 1 ) {

                    vals = _.without(vals, val.toString());
                    filter_obj[key] = _.uniq(vals).join('-');

                }
            }
        } else {
            delete filter_obj[key];
        }

        var new_filter = $.param( _.compactObject( filter_obj ) );

        return new_filter;
    };


    var addFilter = function(key, val, multi) {
        multi = multi || false;
        var new_filter = this.setFilter(key, val, multi);

        Backbone.history.navigate(new_filter, {trigger: true});
        return true;
    };


    var removeFilter = function(key, val, multi) {
        multi = multi || false;
        var new_filter = this.unsetFilter(key, val, multi);

        Backbone.history.navigate(new_filter, {trigger: true});
        return true;
    };


    var getServerQueryString = function(filter) {
        var output = '';
        output = setFilter('current_category', Emart.current_category);

        return output;
    };


    var setCookie = function(key, val) {
        $.cookie(key, val, { expires: 7, domain: Emart.domain, path: '/' });
        return true;
    };


    var getCookie = function(key) {
        return $.cookie(key);
    };


    var removeCookie = function(key) {
        $.removeCookie(key, { domain: Emart.domain, path: '/' });
        return true;
    };


    return {
        urldecode: urldecode,
        parseQueryString: parseQueryString,
        setFilter: setFilter,
        addFilter: addFilter,
        unsetFilter: unsetFilter,
        removeFilter: removeFilter,
        getServerQueryString: getServerQueryString,

        setCookie: setCookie,
        getCookie: getCookie,
        removeCookie: removeCookie
    };

});
