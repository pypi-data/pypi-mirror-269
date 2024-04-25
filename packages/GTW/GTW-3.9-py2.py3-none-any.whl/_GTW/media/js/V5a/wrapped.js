// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped.js
//
// Purpose
//    Vanilla javascript wrapper for document nodes
//
// Revision Dates
//    23-Jan-2016 (CT) Creation
//    27-Jan-2016 (CT) ...Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$ = $.Wrapped = function Wrapped (arg, context) {
        if (! (this instanceof $.$$ )) {
            // Make it usable without explicit `new`
            return new $.$$ (arg, context);
        };

        if (typeof arg === "string") {
            // select nodes of context matching arg
            arg = $.select (arg, context);
        } else if (arg && arg.nodeName) {
            // put single node into array
            arg = [arg];
        };

        if (! Array.isArray (arg)) {
            arg = $.as_array (arg || []); // convert to javascript array
        };

        this.wrapped = arg;
        this.length  = arg.length;
        return this;
    };

    $.$$.prototype.wrapped = [];

    $.$$.prototype.for_each = function for_each (cb) {
        this.wrapped.forEach (cb, this);
        return this;
    };

    $.$$.prototype.for_each_arg = function for_each_arg (arg, cb) {
        var args = $.arg_to_array (arg);
        function one (node) {
            args.forEach (function (a) { cb.call (this, node, a); }, this)
        };
        return this.for_each (one);
    };

    $.$$.get = function get (i) {
        return new $.$$ (this.wrapped [i || 0]);
    };

    $.$$.hide = function hide () {
        return this.for_each (function (n) { n.style.display = "none"; });
    };

    $.$$.show = function show () {
        return this.for_each (function (n) { n.style.display = ""; });
    };

  } ($V5a)
);

// __END__ V5a/wrapped.js
