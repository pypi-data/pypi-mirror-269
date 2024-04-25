// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/new_window.js
//
// Purpose
//    Open a new window that can't tab-nab
//
// Revision Dates
//     5-May-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.new_window = function new_window (href) {
        // reset `opener` to disable tab-nabbing
        // cf. https://mathiasbynens.github.io/rel-noopener/
        var result = window.open ();
        result.opener = null; ;
        if (href) {
            result.location = href;
            result.focus ();
        };
        return result;
    };
  } ($V5a)
);

// __END__ V5a/new_window.js
