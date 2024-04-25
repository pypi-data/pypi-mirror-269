//-*- coding: utf-8 -*-
// Copyright (C) 2010-2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW_util
//
// Purpose
//    Utility javascript functions for GTW
//
// Revision Dates
//     3-Aug-2010 (CT) Creation (`as_int_array`)
//     4-Aug-2010 (CT) `fix_a_nospam` added (factored from GTW.jQuery)
//    10-Oct-2010 (CT) `GTW_Externalize` added
//    19-Nov-2010 (CT) `push_history` added
//    20-Jan-2011 (CT) Rename functions `GTW_Externalize` to `gtw_externalize`
//    26-Jan-2011 (CT) Style change
//     5-Apr-2011 (CT) `Array.prototype.indexOf` defined, if necessary
//    14-Oct-2011 (MG) Missing `var` added to `as_int_array`
//    22-Feb-2012 (CT) Change `fix_a_nospam` to take data from `next` `b.nospam`
//    29-Apr-2013 (CT) Move `gtw_externalize` and `fix_a_nospam` to `jQ/util.js`
//    29-Apr-2013 (CT) Add `show_message`
//     1-May-2014 (CT) Change `show_message` to use `inspect.show` if available
//    15-Jan-2015 (CT) Use `String.match`, not `String.search`
//    20-Jan-2016 (CT) Delegate to $V5a.history_push, remove obsolete functions
//    ««revision-date»»···
//--

( function () {
    "use strict";

    $GTW.update
        ( { push_history   : function (url, title, state) {
                return $V5a.history_push (url, title, state);
            }
          , show_message   : function show_message () {
                var args = [].slice.apply (arguments); // convert to real array
                var msg, parts = [];
                if ("inspect" in $GTW) {
                    for (var i = 0, li = args.length, a; i < li; i++) {
                        a = args [i];
                        parts.push ($GTW.inspect.show (a));
                    };
                    msg = parts.join ("\n");
                } else {
                    msg = args.join  (" ");
                };
                alert (msg);
            }
          }
        );
  } ()
);

// __END__ GTW_util.js
