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
//    GTW_week_roller
//
// Purpose
//    jQuery plugin for a calendar displayed as week_roller
//
//
// Revision Dates
//    15-Nov-2010 (CT) Creation
//    16-Nov-2010 (CT) `change_field` factored
//    16-Nov-2010 (CT) `init_cal` added and used
//    17-Nov-2010 (CT) `init_cal` changed to use AJAX `.load` to fill `div$`
//    19-Nov-2010 (CT) `push_history` called
//    26-Nov-2010 (CT) `init_slider` added and used
//    27-Nov-2010 (CT) Handling of `.echo` added
//    30-Nov-2010 (CT) Handling of `.echo` changed
//    20-Jan-2011 (CT) Rename function `GTW_week_roller` to `gtw_week_roller`
//    26-Jan-2011 (CT) Style change
//    30-Nov-2011 (CT) Use `return false` instead of .`preventDefault`
//     5-Apr-2013 (CT) Adapt to API changes of jQueryUI 1.9+
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    20-Jan-2016 (CT) Use `$V5a.history_push`, not `$GTW.push_history`
//    ««revision-date»»···
//--

( function ($) {
    "use strict";

    $.fn.gtw_week_roller = function (options) {
        options = $.extend
            ( { apply_button_name      : "Apply"
              , cal_selector           : "table.calendar"
              , ctrl_selector          : "form.ctrl"
              , day_as_html            : true
              , selected_class         : "selected"
              , day_selector           : "td"
              , slider_ctrl_selector   : ".slider-ctrl"
              , slider_echo_selector   : ".slider-echo"
              , slider_msg_selector    : ".slider-echo .message p"
              , today_selector         : "td.today"
              , q_day_transformer      : function (href)
                  { return href.replace (/(\d{4}\/\d{1,2}\/\d{1,2})/, "qx/$1"); }
              , q_url_transformer      : function (name)
                  { return name.replace (/\/q/, "/qx"); }
              }
            , options || {}
            );
        var change_field = function (name, context, response, value) {
            $("input[name='" + name + "']", context).attr
                ("value", (value != null) ? value : response [name]);
        };
        var fieldv = function (name, context) {
            return $("input[name='" + name + "']", context).attr ("value");
        };
        var i2s = function (value) {
            return (value < 10 ? "0" : "") + value;
        };
        var init_cal = function (wr$) {
            var cal$   = $(options.cal_selector, wr$);
            var div$   = $("div." + options.selected_class, wr$);
            var today$ = $(options.today_selector, cal$);
            $(options.day_selector, cal$).each (
                function () {
                    var day  = this;
                    var day$ = $(day);
                    var href = $("span.date a", day$).attr ("href");
                    if (href) {
                        var qx = options.q_day_transformer (href);
                        day$.click (
                            function (ev) {
                                div$.html ("");
                                if (options.day_as_html) {
                                    div$.load (qx).css ({display : "block"});
                                } else {
                                    $.getJSON
                                      ( qx, null
                                      , function (response) {
                                            if (response) {
                                                div$.html (response.html)
                                                    .css  ({display : "block"});
                                            };
                                        }
                                      );
                                };
                                if (options.selected) {
                                    $(options.selected).removeClass
                                        (options.selected_class);
                                };
                                day$.addClass (options.selected_class);
                                options.selected = day;
                                return false;
                            }
                        );
                    };
                }
            );
            today$.triggerHandler ("click");
            place_slider (wr$);
        };
        var init_ctrl = function (wr$) {
            $(options.ctrl_selector, wr$).each (
                function () {
                    var ctrl$ = $(this);
                    var cal$  = $(options.cal_selector, wr$);
                    var q_url = this.action;
                    var x_url = options.q_url_transformer (q_url);
                    $("input[type='submit']", ctrl$).click (
                        function (ev) {
                            var args = ctrl$.serialize ()
                                  + "&" + this.name + "=" + this.value;
                            $.getJSON
                              ( x_url
                              , args
                              , function (response) {
                                    if (response) {
                                        cal$.replaceWith (response.calendar);
                                        change_field ("day",   ctrl$, response);
                                        change_field ("month", ctrl$, response);
                                        change_field ("weeks", ctrl$, response);
                                        change_field ("year",  ctrl$, response);
                                        cal$ = $(options.cal_selector, wr$);
                                        init_cal (wr$);
                                        $V5a.history_push (q_url + "?" + args);
                                    };
                                }
                              );
                            return false;
                        }
                    );
                }
            );
            init_slider (wr$);
            init_cal    (wr$);
        };
        var init_slider = function (wr$) {
            $(options.slider_ctrl_selector, wr$).each (
                function () {
                    var apply$  =
                        $("input[name='"+options.apply_button_name+"']", wr$);
                    var slider_ctrl$ = $(this);
                    var slider_echo$ = $(options.slider_echo_selector, wr$);
                    var slider_msg$  = $(options.slider_msg_selector,  wr$);
                    var anchor$      = $("span.anchor", slider_msg$);
                    var weeks$       = $("span.weeks",  slider_msg$);
                    var adate, tdate;
                    var change = function (event, ui) {
                          var value = - Math.round (ui.value);
                          if (value) {
                              change_field          ("delta", wr$, null, value);
                              apply$.triggerHandler ("click");
                              change_field          ("delta", wr$, null, "");
                              slider_ctrl$.slider   ("value", 0);
                          };
                    };
                    var slide = function (event, ui) {
                          var value = - Math.round (ui.value);
                          var delta_ms = value * 7 * 86400 * 1000;
                          tdate = new Date (adate.getTime () + delta_ms);
                          change_field ("delta", wr$, null, value || "");
                          weeks$.html  (value);
                          anchor$.html
                              ( tdate.getFullYear ()
                              + "/"
                              + i2s (tdate.getMonth () + 1)
                              + "/"
                              + i2s (tdate.getDate ())
                              );
                    };
                    var start = function (event, ui) {
                        var cal$ = $(options.cal_selector, wr$);
                        adate = new Date
                            ( fieldv ("year",  wr$)
                            , fieldv ("month", wr$) - 1
                            , fieldv ("day",   wr$)
                            );
                        slider_echo$
                            .addClass ("enabled")
                            .css
                                ( { height    : cal$.css ("height")
                                  , width     : cal$.css ("width")
                                  }
                                )
                            .position
                                ( { my        : "center"
                                  , at        : "center"
                                  , of        : options.cal_selector
                                  , collision : "fit"
                                  }
                                );
                        slider_msg$.position
                            ( { my        : "center"
                              , at        : "center"
                              , of        : options.cal_selector
                              }
                            );
                        slide (event, ui);
                    };
                    var stop = function (event, ui) {
                        slider_echo$.removeClass ("enabled");
                        weeks$.html  ("");
                        anchor$.html ("");
                    };
                    slider_ctrl$.slider
                        ( { max         : 53
                          , min         : -53
                          , orientation : "vertical"
                          , value       : 0
                          , change      : change
                          , slide       : slide
                          , start       : start
                          , stop        : stop
                          }
                        );
                    slider_ctrl$.addClass ("enabled");
                    $(".ui-slider-handle", slider_ctrl$).append
                        ("<span class='ui-icon ui-icon-triangle-2-n-s'></span>");
                }
            );
        };
        var place_slider = function (wr$) {
            $(options.slider_ctrl_selector, wr$)
                .css ("height", $(options.cal_selector, wr$).css ("height"))
                .position
                    ( { my     : "left+5"
                      , at     : "right"
                      , of     : options.cal_selector
                      }
                    );
        };
        $(this).each (function () { init_ctrl ($(this)); });
        return this;
    };
  }
) (jQuery);

// __END__ GTW_week_roller.js
