// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/parse_html.js
//
// Purpose
//    Vanilla javascript function parsing a string containing html into an
//    element
//
// Revision Dates
//    27-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.parse_html = function parse_html (s) {
        var result = document.createElement ("div");
        result.outerHTML = s;
        return result;
    };
  } ($V5a)
);

// __END__ V5a/parse_html.js
