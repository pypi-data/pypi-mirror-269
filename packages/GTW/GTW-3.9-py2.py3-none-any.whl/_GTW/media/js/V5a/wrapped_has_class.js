// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_has_class.js
//
// Purpose
//    Vanilla javascript wrapper functions returning elements of wrapped set
//    having some or all specified classes
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype._filter_has_class = function (class_spec, tester, invert) {
        var classes = $.arg_to_array (class_spec);
        var result  = this.filter
            ( function (node) {
                var result = tester.call
                    ( classes
                    , function (name) { return node.classList.contains (name); }
                    );
                if (invert) {
                    result = ! result;
                };
                return result;
              }
            , this
            );
        return result;
    };

    $.$$.prototype.has_class_all = function has_class_all (class_spec) {
        return this._filter_has_class (class_spec, Array.prototype.every);
    };

    $.$$.prototype.has_class_any = function has_class_any (class_spec) {
        return this._filter_has_class (class_spec, Array.prototype.some);
    };

    $.$$.prototype.has_class_none = function has_class_none (class_spec) {
        return this._filter_has_class (class_spec, Array.prototype.some, "!");
    };
  } ($V5a)
);

// __END__ V5a/wrapped_has_class.js
