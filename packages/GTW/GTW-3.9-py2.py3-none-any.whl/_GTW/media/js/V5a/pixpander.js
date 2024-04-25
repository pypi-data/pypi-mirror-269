// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/pixpander.js
//
// Purpose
//    Vanilla javascript function expanding linked images in place
//
// Revision Dates
//    17-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.pixpander = $.merge
        ( function pixpander (opts) {
            var O    = $.merge ({}, pixpander.defaults,  opts);
            var S    = $.merge ({}, pixpander.selectors, O ["selectors"]);
            var els  = $.query (S.img);
            function show (ev, img, url, style, width) {
                img.src   = url;
                img.width = width || "auto";
                img.setAttribute ("style", style);
                O.x_class && img.classList.toggle (O.x_class);
            };
            $.for_each
                ( els
                , function (img) {
                    var link  = img.parentNode;
                    var href  = link.href;
                    var src   = img.src;
                    var style = img.style.cssText;
                    var width = img.clientWidth;
                    $.bind
                        ( link, "click"
                        , function pixpander_cb (ev) {
                            if (img.src === src) {
                                show (ev, img, href, "",   "auto");
                            } else {
                                show (ev, img, src,  style, width);
                            };
                            $.prevent_default (ev);
                          }
                        );
                  }
                );
          }
        , { defaults  :
              { x_class   : "pixpanded"
              }
          , selectors :
              { img       : "a[href$='.jpg'] > img, a[href$='.png'] > img"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/pixpander.js
