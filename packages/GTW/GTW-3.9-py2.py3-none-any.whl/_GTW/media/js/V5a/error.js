// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/error.js
//
// Purpose
//    Vanilla javascript function displaying an error
//
// Revision Dates
//    27-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.error = function error (msg) {
        if (self.console) {
            console.error.apply (console, arguments);
        } else {
            alert (msg);
        };
    };
  } ($V5a)
);

// __END__ V5a/error.js
