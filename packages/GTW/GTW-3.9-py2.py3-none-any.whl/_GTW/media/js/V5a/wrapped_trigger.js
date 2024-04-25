// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_trigger.js
//
// Purpose
//    Trigger an event for all elements of a wrapped set
//
// Revision Dates
//    25-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.trigger = function trigger (ev_name, ev_opts, EV_Type) {
        var ev = $.create_event (ev_name, ev_opts, EV_Type);
        return this.for_each (function (n) { n.dispatchEvent (ev); });
    };
  } ($V5a)
);

// __END__ V5a/wrapped_trigger.js
