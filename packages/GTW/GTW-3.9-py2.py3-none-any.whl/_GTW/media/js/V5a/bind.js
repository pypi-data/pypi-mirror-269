// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/bind.js
//
// Purpose
//    Bind and unbind event listeners for an element or a list of elements.
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    24-Jan-2016 (CT) Remove list handling from `bind`
//    24-Jan-2016 (CT) Factor `_bind`, `event_map`
//    25-Jan-2016 (CT) Factor `_unbind`
//    26-Jan-2016 (CT) Restrict `bind_map` to name-spaced event-names
//    ««revision-date»»···
//--

// bind has the signature:
// target     : a single element or a list of elements
// ev_spec    : a string of space-separated event names
// handler    : a function to execute each time the event is triggered
// capture    : a boolean indicating whether to capture the event
//
// alternatively, bind also supports the signature:
// target     : a single element or a list of elements
// ev_spec    : a object containing mapping ev_spec keys to handler values
// null
// capture    : a boolean indicating whether to capture the event
//
// event names can contain namespace indicators separated by a period.
// Namespacing allows to unbind some event handlers of a specific event name
// without affecting others

;
( function ($) {
    "use strict";

    var bind_map = {};

    function add (target, ev_key, ev_name, cb, capture) {
        if (ev_key != ev_name) {
            var bindings;
            if (ev_key in bind_map) {
                bindings = bind_map [ev_key];
            } else {
                bindings = bind_map [ev_key] = [];
            };
            bindings.push ([ev_name, cb, capture]);
        };
        target.addEventListener (ev_name, cb, capture);
    };

    $._bind = function _bind (target, ev_map, capture) {
        capture = capture || false;
        for (var ev_key in ev_map) {
            var cb      = ev_map [ev_key];
            var ev_name = ev_key.split (".") [0];
            add (target, ev_key, ev_name, cb, capture);
        };
    };

    $._unbind = function _unbind (target, ev_list) {
        ev_list.forEach
            ( function (ev_key) {
                if (ev_key in bind_map) {
                    var bindings = bind_map [ev_key], el;
                    for (var i = 0, li = bindings.length, args; i < li; i++) {
                        args = bindings [i];
                        target.removeEventListener.apply (target, args);
                    };
                    delete bind_map [ev_key];
                };
              }
            );
    };

    $.bind = function bind (target, ev_spec, handler, capture) {
        var ev_map = $.event_map (ev_spec, handler);
        $._bind (target, ev_map, capture);
    };

    $.unbind = function unbind (target, ev_spec) {
        var ev_list = $.arg_to_array (ev_spec);
        $._unbind (target, ev_list);
    };
  } ($V5a)
);

// __END__ V5a/bind.js
