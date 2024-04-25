// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/event_map.js
//
// Purpose
//    Vanilla javascript function returning an event-map for bind arguments
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.event_map = function event_map (ev_spec, handler) {
        var map    = {};
        var result = {};
        if (handler === null || handler === undefined) {
            map = ev_spec;
        } else {
            map [ev_spec] = handler;
        };
        Object.keys (map).forEach
            ( function (ev_spec) {
                var cb = map [ev_spec];
                $.arg_to_array (ev_spec).forEach
                    (function (ev_name) { result [ev_name] = cb; });
              }
            );
        return result;
    };
  } ($V5a)
);

// __END__ V5a/event_map.js
