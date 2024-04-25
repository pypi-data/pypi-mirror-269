// Copyright (C) 2011-2015 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/hd_input.js
//
// Purpose
//    jQuery plugin to support input fields with display different from value
//
// Revision Dates
//    28-Nov-2011 (CT) Creation
//     7-Dec-2011 (CT) Change plugin name to `gtw_hd_input`
//     7-Mar-2012 (CT) Add `hidden`, set `disabled` of `hidden` to `false`, too
//    10-Apr-2013 (CT) Add and use `closing_flag`
//     3-May-2014 (CT) Add and use `trigger_event`, not hard-coded "focus"
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    15-Jan-2015 (CT) Add handling of `trigger_event` for keys,
//                     add `clear_callback`
//    26-Mar-2015 (CT) Prevent default for cursor moving keys only
//                     in `hd_input_trigger_key`
//    ««revision-date»»···
//--

( function ($, undefined) {
    "use strict";

    $.fn.gtw_hd_input = function (opts) {
        var self      = this;
        var selectors = $.extend
            ( { display       : ".value.display"
              , hidden        : ".value.hidden"
              }
            , opts && opts ["selectors"] || {}
            );
        var options   = $.extend
            ( { closing_flag  : "gtw_hd_input_closing"
              , key_ignore_hi : 39               // cursor right
              , key_ignore_lo :  9               // tab
              , key_trigger   : {38 : 1}         // cursor up
              , trigger_event : "focus"
              }
            , opts || {}
            , { selectors     : selectors
              }
            );
        var display$ = $(selectors.display, this);
        var hidden$  = $(selectors.hidden,  this);
        var hd_callback;
        if ("callback" in options) {
            if (options.trigger_event.match (/\bkey(?:down|press|up)\b/)) {
                hd_callback = function hd_input_trigger_key (ev) {
                    var closing = self.data (options.closing_flag);
                    if (closing) {
                        return false;
                    } else {
                        var k      = ev.which;
                            // Unicode value of key pressed
                            //   8     backspace (delete backwards key)
                            //   9     tab
                            //  10     new line
                            //  13     carriage return
                            //  16     shift key
                            //  17     control key
                            //  18     alt key
                            //  27     escape
                            //  32     space
                            //  33     page up           (mini keypad)
                            //  34     page down         (mini keypad)
                            //  35     end               (mini keypad)
                            //  36     home              (mini keypad)
                            //  37     cursor left
                            //  38     cursor up
                            //  39     cursor right
                            //  40     cursor down
                            //  45     insert            (mini keypad)
                            //  46     delete            (mini keypad)
                            // 127     backspace
                        var ignore =
                            (  k >= options.key_ignore_lo
                            && k <= options.key_ignore_hi
                            && ! (k in options.key_trigger)
                            );
                        var result = ignore;
                        if (! ignore) {
                            result = options.callback.apply (this, arguments);
                            if (ev && "preventDefault" in ev) {
                                if (k >= 33 && k <= 40) {
                                    // without this, cursor-up and cursor-down
                                    // cause scrolling
                                    ev.preventDefault ();
                                };
                            };
                            if ("clear_callback" in options) {
                                if (k in {8 : 1, 46 : 1, 127: 1}) {
                                    options.clear_callback.apply
                                        (this, arguments);
                                };
                            };
                        };
                        return result;

                    };
                };
            } else {
                hd_callback = function hd_input_trigger (ev) {
                    var closing = self.data (options.closing_flag);
                    if (closing) {
                        return false;
                    } else {
                        return options.callback.apply (this, arguments);
                    };
                };
            };
            display$.bind (options.trigger_event, hd_callback);
        };
        display$.prop ("disabled", false);
        hidden$.prop  ("disabled", false);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/hd_input.js
