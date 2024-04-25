// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/select.js
//
// Purpose
//    Vanilla javascript function to select specific elements
//
// Revision Dates
//    23-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.select = function select (expr, context) {
        if (! context) {
            // try specific selection functions (these don't support context)
            if (/^\.[\w\-]+$/.test (expr)) {
                return document.getElementsByClassName (expr);
            } else if (/^\w+$/.test (expr)) {
                return document.getElementsByTagName (expr);
            } else if (/^\#[\w\-]+$/.test (expr)) {
                return [document.getElementById (expr)];
            };
        };
        return (context || document).querySelectorAll (expr);
    };
  } ($V5a)
);

// __END__ V5a/select.js
