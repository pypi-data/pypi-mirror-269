// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_reduce.js
//
// Purpose
//    Vanilla javascript wrapper merging all nodes returned by callback
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.reduce = function reduce (cb) {
        var result = $.$$
            ( this.wrapped.reduce
                ( function (ns, node, i) {
                    return ns.concat (cb (node, i));
                  }
                , []
                )
            );
        return result;
    };
  } ($V5a)
);

// __END__ V5a/wrapped_reduce.js
