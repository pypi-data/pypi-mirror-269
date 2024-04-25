// Copyright (C) 2016-2017 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/scroll_to.js
//
// Purpose
//    Vanilla javascript functions for scrolling an element in a container
//
// Revision Dates
//    21-Jan-2016 (CT) Creation
//    30-Dec-2016 (CT) Rename `scroll_to` to `_scroll_to` to avoid name clash
//                     inside `$.scroll_to`
//    21-Jan-2017 (CT) Add and use `scrolling_parent`, add argument `off`
//                     + simplify `_scroll_to`
//    21-Jan-2017 (CT) Fix `scroll_to` for `scrolling_parent == documentElement`
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var scroll_min = 0;
    var spec       =
        { left     :
            { scroll_pos     : "scrollLeft"
            , side           : "left"
            , size           : "width"
            }
        , top      :
            { scroll_pos     : "scrollTop"
            , side           : "top"
            , size           : "height"
            }
        };
    function _scroll_to (S, el, rel_pos, off) {
        var el_bcr   = el.getBoundingClientRect () ;
        var sp       = $.scrolling_parent       (el);
        var sp_bcr   = sp.getBoundingClientRect ();
        var offset   = (off || 0) + Math.max
            ((sp_bcr [S.size] - el_bcr [S.size]) * (rel_pos || 0), 0);
        var delta    = el_bcr [S.side] - offset;
        if (sp === document.documentElement) {
            var arg = {}; arg [S.side] = delta;
            window.scrollBy (arg);
        } else {
            sp [S.scroll_pos] += delta;
        };
    };
    $.scrolling_parent = function scrolling_parent (el) {
        var parent = el.parentElement;
        var result = document.documentElement;
        while (parent !== null) {
            if (parent.scrollWidth != parent.offsetWidth) {
                result = parent;
                break;
            };
            parent = parent.parentElement;
        };
        return result;
    };
    $.scroll_to_h = function scroll_to_h (el, rel_pos, off) {
        _scroll_to (spec.left, el, rel_pos, off);
    };
    $.scroll_to_v = function scroll_to_v (el, rel_pos, off) {
        _scroll_to (spec.top,  el, rel_pos, off);
    };
    $.scroll_to = function scroll_to (el, rel_pos_h, off_h, rel_pos_v, off_v) {
        _scroll_to (spec.left, el, rel_pos_h, off_h);
        _scroll_to (spec.top,  el, rel_pos_v, off_v);
    };
  } ($V5a)
);

// __END__ V5a/scroll_to.js
