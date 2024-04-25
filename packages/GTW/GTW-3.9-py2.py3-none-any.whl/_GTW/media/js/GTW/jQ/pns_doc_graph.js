// Copyright (C) 2012-2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/pns_doc_graph.js
//
// Purpose
//    jQuery plugin to enhance svg-graph displaying a package namespace's
//    object graph
//
// Revision Dates
//    25-Sep-2012 (CT) Creation
//    26-Sep-2012 (CT) Use `.click` not `.on` to bind `cb_click_node`
//     5-May-2016 (CT) Use `$V5a.new_window`, not home-grown code
//    ««revision-date»»···
//--

;
( function ($, undefined) {
    "use strict";
    $.fn.gtw_pns_doc_graph = function gtw_pns_doc_graph (opts) {
        var selectors = $.extend
            ( { node  : "g.E_Type[id]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( {
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        var cb_click_node = function cb_click_node (ev) {
            var target$ = $(ev.target).closest (selectors.node);
            var name    = target$.attr ("id");
            var url     = options.qurl + name;
            $V5a.new_window (url);
        };
        options.svg$ = this;
        this.find  (selectors.node)
            .click (cb_click_node)
            .css   ("cursor", "pointer");
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/pns_doc_graph.js
