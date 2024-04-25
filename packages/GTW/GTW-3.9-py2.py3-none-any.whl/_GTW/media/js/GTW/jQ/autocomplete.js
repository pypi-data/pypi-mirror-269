// Copyright (C) 2011-2014 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    autocomplete
//
// Purpose
//    Wrap jquery-ui.autocomplete
//
// Revision Dates
//    13-Oct-2011 (CT) Creation
//    31-Jan-2013 (MG) Fix changing of `_renderItem` to work with new
//                     jQueryUI versions
//     5-Apr-2013 (CT) Adapt to API changes of jQueryUI 1.9+
//     9-May-2014 (CT) Remove unused `$GTW.L`
//    14-May-2014 (CT) Change `renderer` to handle `disabled`
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    ««revision-date»»···
//--

( function ($) {
    "use strict";

    var renderer =
        { html          : function _ac_render_item_html (ul, item) {
              var contents, result;
              if ("disabled" in item) {
                  contents = $("<i class=\"disabled\">").html (item.label);
              } else {
                  contents = $("<a>").html (item.label);
              };
              result = $("<li>")
                  .data     ("ui-autocomplete-item", item)
                  .append   (contents)
                  .appendTo (ul);
              return result;
          }
        , orig          : $.ui.autocomplete.prototype._renderItem
        };
    $.fn.gtw_autocomplete = function (opts, render_item) {
        var ri = render_item;
        if (typeof ri === "string") {
            ri = renderer [render_item];
        };
        this.each
            ( function setup_autocomplete (n) {
                var self = $(this);
                self.autocomplete (opts);
                if (ri) {
                    var data = self.data ("uiAutocomplete");
                    data._renderItem = ri;
                };
              }
            );
        return this;
    };
  } (jQuery)
);

// __END__ autocomplete.js
