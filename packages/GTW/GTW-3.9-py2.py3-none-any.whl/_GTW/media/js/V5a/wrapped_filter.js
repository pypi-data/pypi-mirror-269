// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_filter.js
//
// Purpose
//    Vanilla javascript filter method for $V5a.wrapped
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.filter = function filter (arg) {
        var pred =
            ( (typeof arg === "function")
            ? function (node) { return arg (node); }
            : function (node) { return $.matches (node, arg || "*"); }
            )
        return new $.$$ (this.wrapped.filter (pred));
    };
  } ($V5a)
);

// __END__ V5a/wrapped_filter.js
