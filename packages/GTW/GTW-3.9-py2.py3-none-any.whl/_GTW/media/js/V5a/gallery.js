// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/gallery.js
//
// Purpose
//    Vanilla javascript functions displaying a photo gallery
//
// Revision Dates
//    20-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.gallery = $.merge
        ( function gallery (opts, context) {
            var O        = $.merge ({}, $.gallery.defaults,  opts);
            var S        = $.merge
                ( { inline      : "." + O.inline_class }
                , $.gallery.selectors
                , O ["selectors"]
                );
            var controls = $.merge
                ( {}
                , $.gallery.controls
                , O ["controls"]
                );
            var g_els    = $.query (S.gallery, context);
            function one_gallery (gallery_el) {
                var current         = 0;
                var inline_el       = $.query1 (S.inline,         gallery_el);
                var photo_el        = $.query1 (S.selected_photo, gallery_el)
                var th_container_el = $.query1 (S.thumbnails,     gallery_el);
                var play_controls   = $.query  (controls.play,    gallery_el);
                var thumbnail_els   = $.query  (S.thumb,     th_container_el);
                var timer_cb;
                var cb              =
                  { head            : function (ev) {
                      return show (0, ev);
                    }
                  , next            : function (ev) {
                      return show (current + 1, ev);
                    }
                  , photo_click     : function (ev) {
                      var result;
                      if (timer_cb) {
                          result = cb.stop (ev);
                      } else {
                          var box     = this.getBoundingClientRect ();
                          var w_fifth = box.width / 5;
                          var x       = ev.clientX;
                          if (x < box.left + w_fifth) {
                              result = cb.prev (ev);
                          } else if (x > box.left + 2 * w_fifth) {
                              result = cb.next (ev);
                          };
                          $.prevent_default (ev);
                      };
                      return result;
                    }
                  , play            : function (ev) {
                      if (timer_cb) {
                          return cb.stop  (ev);
                      } else {
                          return cb.start (ev);
                      };
                    }
                  , prev            : function (ev) {
                      return show (current - 1, ev);
                    }
                  , show            : function (ev) {
                      var i = this.getAttribute ("data-index");
                      cb.stop (ev);
                      return show (i, ev);
                    }
                  , start           : function (ev) {
                      if (! timer_cb) {
                          timer_cb = window.setInterval (cb.next, O.delay);
                          $.for_each
                              ( play_controls
                              , function (play_control) {
                                  var btn = $.query1 (S.btn, play_control);
                                  btn.classList.add    (O.btn_class_stop);
                                  btn.classList.remove (O.btn_class_play);
                                }
                              );
                      };
                    }
                  , stop            : function (ev) {
                      if (timer_cb) {
                          window.clearInterval (timer_cb);
                          timer_cb = null;
                          $.for_each
                              ( play_controls
                              , function (play_control) {
                                  var btn = $.query1 (S.btn, play_control);
                                  btn.classList.add    (O.btn_class_play);
                                  btn.classList.remove (O.btn_class_stop);
                                }
                              );
                      };
                      $.prevent_default (ev);
                    }
                  , tail            : function (ev) {
                      return show (-1, ev);
                    }
                  };
                function show (index, ev) {
                    var len       = thumbnail_els.length;
                    var alt       = photo_el.alt;
                    var old_th_el = thumbnail_els [current], th_el;
                    var old_index = current;
                    var rel_pos   = O.rel_pos
                    old_th_el.classList.remove (O.selected_class);
                    if (index < 0) {
                        index += len;
                    };
                    current        =  index % len;
                    th_el          = thumbnail_els [current];
                    photo_el.src   = O.url_transformer (th_el.src);
                    photo_el.title = (alt ? alt + ":" : "Photo") +
                        " " + (current+1) + "/" + len;
                    th_el.classList.add (O.selected_class);
                    $.scroll_to_h
                        (th_el, old_index < current ? rel_pos : 1 - rel_pos);
                };
                for (var ck in controls) {
                    if (ck in cb) {
                        ( function (k) {
                            $.$$( controls [k], gallery_el).bind
                                ( "click"
                                , function (ev) {
                                    (k === "play") || cb.stop (ev);
                                    return cb [k] (ev);
                                  }
                                );
                          }
                        ) (ck);
                    };
                };
                $.bind (photo_el, "click", cb.photo_click);
                $.$$ (thumbnail_els)
                    .bind ("click", cb.show)
                    .for_each
                        ( function (el, i) {
                            el.setAttribute ("data-index", i);
                          }
                        );
                th_container_el.classList.add (O.inline_class);
                show (0);
            };
            $.for_each (g_els, one_gallery);
          }
        , { controls  :
              { head            : "button.first"
              , next            : "button.next"
              , play            : "button.play"
              , prev            : "button.prev"
              , tail            : "button.last"
              }
          , defaults  :
              { btn_class_play  : "fa-play"
              , btn_class_stop  : "fa-stop"
              , delay           : 2000
              , inline_class    : "inline"
              , play_class      : "playing"
              , rel_pos         : 1/3
              , selected_class  : "selected"
              , url_transformer : function (name)
                  { return name.replace (/\/th\//, "/im/"); }
              }
          , selectors :
              { btn             : ".fa"
              , gallery         : ".gallery"
              , selected_photo  : ".photo img"
              , thumb           : "img"
              , thumbnails      : ".thumbnails"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/gallery.js
