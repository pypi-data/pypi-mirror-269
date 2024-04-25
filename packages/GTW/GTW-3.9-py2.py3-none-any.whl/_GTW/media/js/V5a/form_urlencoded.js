// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/form_urlencoded.js
//
// Purpose
//    Vanilla javascript function encoding an object as x-www-form-urlencoded
//
// Revision Dates
//    26-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    function ue (s) {
        // leaves characters /[-_.!~*'()]/ as un-encoded as encodeURIComponent
        return encodeURIComponent (s).replace ("%20", "+");;
    };

    $.form_urlencoded = function form_urlencoded (obj) {
        var result = Object.keys
            (obj || {}, function (k) { return ue (k) + "=" + ue (obj [k]); });
        return result.join ("&");
    };
  } ($V5a)
);

// __END__ V5a/form_urlencoded.js
