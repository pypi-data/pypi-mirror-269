// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/type_name.js
//
// Purpose
//    Vanilla javascript function returning the type-name of an object
//
// Revision Dates
//    18-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var pat = /^\[object\s+(.*?)\]$/;

    $.type_name = function type_name (obj) {
        var result;
        if (obj === null) {
            result = "null";
        } else if (obj === undefined) {
            result = "undefined";
        } else {
            var s  = Object.prototype.toString.call (obj);
            result = (s.match (pat) [1] || "").toLowerCase ();
            if (result === "number" && isNaN (obj)) {
                result = "nan";
            };
        };
        return result;
    };
  } ($V5a)
);

// __END__ V5a/type_name.js
