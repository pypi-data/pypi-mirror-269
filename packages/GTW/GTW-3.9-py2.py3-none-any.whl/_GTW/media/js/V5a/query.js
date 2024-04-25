// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/query.js
//
// Purpose
//    Function to Select an element by CSS selector.
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.query  = function query  (expr, context) {
        return (context || document).querySelectorAll (expr);
    };
    $.query1 = function query1 (expr, context) {
        return (context || document).querySelector (expr);
    };
  } ($V5a)
);

// __END__ V5a/query.js
