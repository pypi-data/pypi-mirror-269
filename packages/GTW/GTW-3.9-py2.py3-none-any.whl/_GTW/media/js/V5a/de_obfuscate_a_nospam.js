// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/de_obfuscate_a_nospam.js
//
// Purpose
//    Vanilla javascript function de-obfuscating `a.nospam` elements
//
// Revision Dates
//    15-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.de_obfuscate_a_nospam  = $.merge
        ( function de_obfuscate_a (opts) {
            var O  = $.merge ({}, de_obfuscate_a.defaults,  opts);
            var S  = $.merge ({}, de_obfuscate_a.selectors, O ["selectors"]);
            var ls = $.query (S.link);
            $.for_each
                ( ls
                , function (el) {
                    var pl  = el.parentElement;
                    var dl  = $.query1 (S.data, pl);
                    if (dl != null) {
                        var ia   = $.string_to_int_array  (dl [O.data_attr]);
                        var node = document.createElement ("div");
                        node.innerHTML = String.fromCharCode.apply (null, ia);
                        pl.replaceChild (node.firstChild, el);
                    };
                  }
                );
          }
        , { defaults  :
              { data_attr : "title"
              }
          , selectors :
              { link      : "a.nospam"
              , data      : "b.nospam"
              }
          }
        );
} ($V5a)
);

// __END__ V5a/de_obfuscate_a_nospam.js
