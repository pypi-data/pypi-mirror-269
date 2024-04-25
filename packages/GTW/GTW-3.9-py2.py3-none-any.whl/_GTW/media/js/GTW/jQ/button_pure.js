// Copyright (C) 2014 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/button_pure.js
//
// Purpose
//    jQuery plugin for buttons using purecss
//
// Revision Dates
//    24-Oct-2014 (CT) Creation
//    31-Oct-2014 (CT) Fix `_setOption` for `disabled`
//     2-Dec-2014 (CT) Fix calls of `toggleClass`
//    ««revision-date»»···
//--

;( function ($, undefined) {
    "use strict";

    var default_icon_name_map =
        { ADD         : "plus"
        , APPLY       : "check"
        , CANCEL      : "close"
        , CLEAR       : "eraser"
        , CLOSE       : "check"
        , CONFIG      : "wrench"               // "gear"
        , COPY        : "copy"
        , DELETE      : "trash"
        , DISABLE     : "minus-circle"
        , DISPLAY     : "eye"
        , DONE        : "check"
        , DOWN        : "angle-down"
        , FILTER      : "filter"
        , EDIT        : "pencil"
        , ENABLE      : "plus-circle"
        , FIRST       : "angle-double-left"    // "chevron-up"
        , HELP        : "question"
        , INFO        : "info"
        , LAST        : "angle-double-right"   // "chevron-down"
        , NEXT        : "angle-right"          // "chevron-right"
        , PAUSE       : "pause"
        , PLAY        : "play"
        , PREV        : "angle-left"           // "chevron-left"
        , REFRESH     : "refresh"
        , REMOVE      : "trash-o"
        , RESET       : "undo"
        , SELECT      : "pencil"
        , SORT        : "sort"
        , SORT_ASC    : "sort-asc"
        , SORT_DESC   : "sort-desc"
        , UP          : "angle-up"
        };
    var Icon_Map = $GTW.Class.extend
        ( { init        : function init (icon_map) {
              this.defaults = $GTW.FA_Icon_Map.defaults;
              if (icon_map && "map" in icon_map) {
                  this.map         = icon_map.map;
                  this.selectors   = icon_map.selectors;
                  this.icon_class  = icon_map.icon_class;
              } else {
                  this.map         = $.extend
                      ({}, this.defaults, icon_map || {});
                  this.selectors   = { button : "button[name]" };
                  this.icon_class  = {};
                  for (var name in this.map) {
                      if (this.map.hasOwnProperty (name)) {
                          this.selectors [name.toLowerCase () + "_button"] =
                              "button[name=" + name + "]";
                          this.icon_class [name] = "fa-" + this.map [name];
                      };
                  };
              };
            }
          }
        , { defaults    : default_icon_name_map
          }
        );
    $GTW.FA_Icon_Map = Icon_Map;
} (jQuery)
);

;( function ($, undefined) {
    "use strict";

    var button =
        { defaultElement : "<button>"
        , options :
            { click_handler           : null
            , add_icon_class          : null
            , icon_map                : new $GTW.FA_Icon_Map ()
            , icon_selector           : ".fa"
            , suppress_disabled_check : false
            }
        , version : "0.1"
        , _create : function _create () {
              var but$      = this.element;
              var opts      = this.options;
              var click_cb  = this._get_click_cb ();
              var name      = this._get_name     ();
              var icon_map  = this._set_icon_map ();
              var icon_cls  = this._set_icon_cls (name, icon_map);
              var icon$     = this._set_icon     ();
              if (! but$.hasClass ("pure-button")) {
                  but$.addClass  ("pure-button");
              };
              icon$.addClass (icon_cls);
              if (opts.add_icon_class) {
                  icon$.addClass (opts.add_icon_class);
              };
              if (but$.prop  ("disabled") && ! opts.suppress_disabled_check) {
                  this.disable ();
              };
              if (click_cb) {
                  this._on
                      ( opts.suppress_disabled_check
                      , but$
                      , { click : click_cb }
                      );
              };
          }
        , _get_click_cb : function _get_click_cb () {
              return this.options.click_handler;
          }
        , _get_name : function _get_name () {
              var but$ = this.element;
              return but$.data ("name") || but$.prop ("name");
          }
        , _set_icon : function _set_icon () {
              var result = $(this.options.icon_selector, this.element).first ();
              this.icon$ = result;
              return result;
          }
        , _set_icon_cls : function _set_icon_cls (name, icon_map) {
              var result = icon_map.icon_class [name];
              if (result == undefined) {
                  result = name;
              };
              if (result && result.slice (0, 3) != "fa-") {
                  result = "fa-" + result;
              };
              this.icon_cls = result;
              return result;
          }
        , _set_icon_map : function _set_icon_map () {
              var result    = new $GTW.FA_Icon_Map (this.options.icon_map);
              this.icon_map = result;
              return result;
          }
        , _setOption : function _setOption (key, value) {
              var but$ = this.element;
              if (key === "disabled") {
                  if (value) {
                      but$.addClass    ("pure-button-disabled")
                          .attr        ("disabled", "");
                  } else {
                      but$.removeClass ("pure-button-disabled")
                          .removeAttr  ("disabled");
                  };
              };
              this._super (key, value);
          }
        };
    var a_link =
        { defaultElement : "<a>"
        , _get_name : function _get_name () {
              return this._super () || this.options.name;
          }
        };
    var toggle =
        { options :
            { suppress_disabled_check : true
            }
        , toggle : function toggle (ev) {
              var but$          = this.element;
              var click_handler = this.options.click_handler;
              var icon$         = this.icon$;
              var normal        = icon$.hasClass (this.icon_cls);
              icon$
                  .toggleClass (this.icon_cls,     !normal)
                  .toggleClass (this.alt_icon_cls,  normal);
              if (click_handler) {
                  click_handler.apply (this, arguments);
              };
          }
        , _get_alt_name : function _get_alt_name () {
              return this.element.data ("alt-name") || this.options.alt_name;
          }
        , _get_click_cb : function _get_click_cb () {
              return this.toggle;
          }
        , _set_icon_cls : function _set_icon_cls (name, icon_map) {
              var result        = this._super         (name, icon_map);
              var alt_name      = this._get_alt_name  ();
              this.alt_icon_cls = icon_map.icon_class [alt_name];
              return result;
          }
        };
    $.widget ("GTW.gtw_button_pure",                                   button);
    $.widget ("GTW.gtw_a_button_pure",        $.GTW.gtw_button_pure,   a_link);
    $.widget ("GTW.gtw_toggle_button_pure",   $.GTW.gtw_button_pure,   toggle);
    $.widget ("GTW.gtw_a_toggle_button_pure", $.GTW.gtw_a_button_pure, toggle);
} (jQuery)
);

// __END__ GTW/jQ/button_pure.js
