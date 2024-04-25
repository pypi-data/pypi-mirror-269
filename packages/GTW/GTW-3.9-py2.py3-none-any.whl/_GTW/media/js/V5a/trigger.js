// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/trigger.js
//
// Purpose
//    Trigger an event for a single element
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    25-Jan-2016 (CT) Factor `create_event`, try modern API first
//    ««revision-date»»···
//--

// https://developer.mozilla.org/en-US/docs/Web/API/document.createEvent
// https://developer.mozilla.org/en-US/docs/Web/API/Event/Event
// https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/dispatchEvent
// https://developer.mozilla.org/en-US/docs/Web/Events
// https://developer.mozilla.org/en-US/docs/Web/Guide/Events/Creating_and_triggering_events

;
( function ($) {
    "use strict";

    var default_ev_opts = { bubbles : true, cancelable : true };

    $.create_event = function create_event (ev_name, ev_opts, EV_Type) {
        var opts = $.merge ({}, default_ev_opts, ev_opts);
        EV_Type = EV_Type || Event;
        try {
            return new EV_Type (ev_name, opts);
        }  catch (e) {
            var tn = EV_Type.name || "Event";
            var ev = document.createEvent (tn);
            ev.initEvent (ev_name, opts.bubbles, opts.cancelable, opts);
            return ev;
        };
    };

    $.trigger = function trigger (target, ev_name, ev_opts, EV_Type) {
        var ev = $.create_event (ev_name, ev_opts, EV_Type);
        target.dispatchEvent (ev);
    };
  } ($V5a)
);

// __END__ V5a/trigger.js
