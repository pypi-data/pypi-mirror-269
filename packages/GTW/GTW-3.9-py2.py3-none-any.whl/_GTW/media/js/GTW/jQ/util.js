// Copyright (C) 2011-2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    util
//
// Purpose
//    Utility functions for jQuery use
//
// Revision Dates
//    27-Jul-2011 (CT) Creation
//    18-Apr-2013 (CT) Add `alert` to `options.error`
//    29-Apr-2013 (CT) Move `gtw_externalize` and `fix_a_nospam` in here
//    20-Jan-2014 (CT) Pass `xhr_instance.responseText` to `show_message`;
//                     remove call of `alert` from `options.error`
//    15-Apr-2014 (CT) Put request info into `options.error` of `gtw_ajax_2json`
//    30-Apr-2014 (CT) Don't use `jsonify` in `gtw_ajax_2json` for `GET`
//    20-Jan-2016 (CT) Remove `fix_a_nospam`, `gtw_externalize`
//                     * use `$V5a...` instead
//    22-Jan-2016 (CT) Use `JSON.stringify`, not `$GTW.jsonify`
//    ««revision-date»»···
//--


( function ($) {
    "use strict";
    $.gtw_ajax_2json = function (opts, name) {
        var options  = $.extend
            ( { async       : false                  // defaults settings
              , timeout     : 30000
              , type        : "POST"
              }
            , opts                                   // arguments
            , { contentType : "application/json"     // mandatory settings
              , dataType    : "json"
              , processData : false
              }
            );
        var data = options.data;
        if ((options.type != "GET") && (typeof data !== "string")) {
            options.data = JSON.stringify (data);
        };
        if (! ("error" in options)) {
            options.error = function (xhr_instance, status, exc) {
                var msg = (name || "Ajax request") + " failed: ";
                $GTW.show_message
                    ( msg, status, exc
                    , "\n\nRequest:", options.type, options.url
                    , "\n\nResponse:", xhr_instance.responseText
                    );
            };
        };
        $.ajax (options);
    };
  } (jQuery)
);

// __END__ util.js
