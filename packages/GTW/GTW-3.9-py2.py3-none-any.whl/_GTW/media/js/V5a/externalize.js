// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/externalize.js
//
// Purpose
//    Vanilla javascript function opening external links in separate window
//
// Revision Dates
//    18-Jan-2016 (CT) Creation
//     5-May-2016 (CT) Reset `opener` of new window to disable tab-nabbing
//     5-May-2016 (CT) Factor `$V5a.new_window`
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.externalize = $.merge
        ( function externalize (opts) {
            var O   = $.merge ({}, externalize.defaults,  opts);
            var S   = $.merge ({}, externalize.selectors, O ["selectors"]);
            var ls$ = $.$$    (S.external).has_class_none (O.skip_classes);
            ls$ .add_class (O.x_class)
                .bind
                    ( "click"
                    , function (ev) {
                        $.new_window (this.href);
                        $.prevent_default (ev);
                      }
                    );
          }
        , { defaults  :
              { skip_classes    : ["internal"]
              , x_class         : "external"
              }
          , selectors :
              { external        :
                  "a[href^='http://'], a[href^='https://'], a[href^='//']"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/externalize.js
