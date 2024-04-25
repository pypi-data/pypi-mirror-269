// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a
//
// Purpose
//    Modular library easing use of vanilla javascript (5)
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    15-Jan-2016 (CT) Add `$` function for jQuery compatibility
//    19-Jan-2016 (CT) Add `for_each`
//    20-Jan-2016 (CT) Add class `js` to, remove class `no-js` from, <html>
//    20-Jan-2016 (CT) Add `prevent_default`, `stop_propagation`, `supports`
//    23-Jan-2016 (CT) Add `arg_to_array`, `as_array`, `slice`
//    24-Jan-2016 (CT) Add `for_each`, use `Function.prototype.call.bind`
//    27-Jan-2016 (CT) Add `filter`
//    ««revision-date»»···
//--

;
( function () {
    "use strict";

    if (! ("$V5a" in self)) {
        var AP  = Array.prototype,
            FP  = Function.prototype;
        var rcl = document.documentElement.classList;
        rcl.add    ("js");
        rcl.remove ("no-js");
        self.$V5a =
          { author      : "christian.tanzer@swing.co.at"
          , copyright   : "Copyright (C) 2016 Christian Tanzer"
          , license     : "https://www.gg32.com/license/bsd_3c.html"
          , supports    : {}
          , version     : "1.0"

          , arg_to_array : function arg_to_array (arg) {
                // convert `arg` denoting one or more names or event-types to
                // an array of non-null names/event-types
                var result =
                    ( (typeof arg === "string")
                    ? arg.split (/[\s,]+/) // possible separators: space, comma
                    : $V5a.as_array (arg)
                    ).filter (function (e) { return e.length; });
                return result;
            }
          , as_array : function as_array (arg) {
                return $V5a.slice (arg, 0)
            }
          , filter   : FP.call.bind (AP.filter)
          , for_each : FP.call.bind (AP.forEach)
          , prevent_default : function prevent_default (ev) {
                try { ev.preventDefault (); } catch (e) {};
            }
          , ready : function ready (cb) {
                if (document.readyState !== "loading") {
                    cb ();
                } else {
                    document.addEventListener ("DOMContentLoaded", cb);
                };
            }
          , slice : FP.call.bind (AP.slice)
          , stop_propagation : function stop_propagation (ev) {
                try { ev.stopPropagation (); } catch (e) {};
            }
          };
        if (! ("$" in self)) {
            // jQuery compatibility
            self.$ = self.$V5a.ready;
        };
    };
  } ()
);

// __END__ V5a.js
