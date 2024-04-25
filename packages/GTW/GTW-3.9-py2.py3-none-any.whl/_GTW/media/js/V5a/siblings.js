// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/siblings.js
//
// Purpose
//    Return all siblings of element
//
// Revision Dates
//    27-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.siblings = function siblings (el) {
        var result = $.filter
            (el.parentNode.children, function (c) { return c !== el; });
        return result;
    };
  } ($V5a)
);

// __END__ V5a/siblings.js
