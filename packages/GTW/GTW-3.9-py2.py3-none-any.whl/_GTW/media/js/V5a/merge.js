// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/merge.js
//
// Purpose
//    Function to merge the values of all enumerable own properties from one or
//    more source objects to a target object.
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    if ("assign" in Object) {
        $.merge = Object.assign;
    } else {
        $.merge = function merge (target) {
            for (var i = 1, li = arguments.length, src; i < li; i++) {
                src = arguments [i];
                if (src !== undefined && src !== null) {
                    for (var k in src) {
                        if (src.hasOwnProperty (k)) {
                            target [k] = src [k];
                        };
                    };
                };
            };
            return target;
        };
    };
  } ($V5a)
);

// __END__ V5a/merge.js
