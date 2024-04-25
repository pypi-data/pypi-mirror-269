// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_add_class.js
//
// Purpose
//    Vanilla javascript wrapper function adding a class to all wrapped nodes
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.add_class = function add_class (class_spec) {
        this.for_each_arg
            (class_spec, function (el, name) { el.classList.add (name); });
        return this;
    };
  } ($V5a)
);

// __END__ V5a/wrapped_add_class.js
