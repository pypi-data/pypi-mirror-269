// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_bind.js
//
// Purpose
//    Bind and unbind event listeners for elements of a wrapped set.
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.bind = function bind (ev_spec, handler, capture) {
        var ev_map = $.event_map (ev_spec, handler);
        return this.for_each (function (n) { $._bind (n, ev_map, capture); });
    };

    $.$$.prototype.unbind = function unbind (ev_spec) {
        var ev_list = $.arg_to_array (ev_spec);
        return this.for_each (function (n) { $._unbind (n, ev_list); });
    };
  } ($V5a)
);

// __END__ V5a/wrapped_bind.js
