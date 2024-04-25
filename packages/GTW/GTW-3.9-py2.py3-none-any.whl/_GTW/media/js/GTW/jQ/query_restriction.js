// Copyright (C) 2011-2017 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/query_restriction.js
//
// Purpose
//    jQuery plugin for a query restriction form
//
// Revision Dates
//    22-Nov-2011 (CT) Creation
//    23-Nov-2011 (CT) Creation continued (new_attr_filter, op_map_by_sym, ...)
//    24-Nov-2011 (CT) Creation continued (disabler_cb, submit_cb)
//    26-Nov-2011 (CT) Creation continued
//                     (setup_obj_list, GTW_buttonify, fix_buttons)
//    28-Nov-2011 (CT) Creation continued (order_by_cb, ...)
//    29-Nov-2011 (CT) Creation continued (order_by...)
//    30-Nov-2011 (CT) Creation continued (ev.delegateTarget)
//     5-Dec-2011 (CT) Creation continued (s/input/:input/ for selectors)
//     6-Dec-2011 (CT) Creation continued (use `gtw_ajax_2json`
//                     [qx_af_html_url, qx_obf_url],
//                     `active_menu_but_class`, `adjust_op_menu`)
//     7-Dec-2011 (CT) Creation continued (`response.callbacks`)
//     7-Dec-2011 (CT) Creation continued (reorganize `options`)
//    12-Dec-2011 (CT) Creation continued (start `setup_completer`)
//    13-Dec-2011 (CT) Creation continued (continue `setup_completer`)
//    15-Dec-2011 (CT) Creation continued (use `$GTW.UI_Icon_Map`,
//                     `.toggleClass`)
//    16-Dec-2011 (CT) Creation continued (factor e_type_selector.js)
//    22-Dec-2011 (CT) s/children/attrs/ (in `attr_filters`)
//    16-Jan-2012 (CT) Creation continued (`attr_select`)
//    17-Jan-2012 (CT) Creation continued (add `focus` to `op_select_cb`)
//    23-Feb-2012 (CT) Use `{ html: XXX }` as argument to `L`
//     8-Mar-2012 (CT) Add `options.completer_position`, `.dialog_position`,
//                     `.menu_position`, adjust positions of various popups
//    19-Mar-2012 (CT) Use `.ui-state-default` in parent of `.ui-icon`
//     5-Apr-2013 (CT) Adapt to API changes of jQueryUI 1.9+
//     5-Apr-2013 (CT) Add gtw-specific prefix to .`data` keys
//     9-Apr-2013 (CT) Add and use `new_menu_nested` for `attr_filters`
//     9-Apr-2013 (CT) Fix dialogs ("gtw_dialog_is_closing")
//    10-Apr-2013 (CT) Bind `beforeClose`, `close` events of `obf$.dialog` to
//                     `order_by.cb.before_close_cb`, `.cb.close_cb`;
//                     bind `cancel_button` to `ob_widget$.dialog("close")`
//    11-Apr-2013 (CT) Add `pred` to `new_menu_nested`
//    11-Apr-2013 (CT) DRY `toggle_disabled_state`, fix it for nested entries;
//                     fix `attr_select.prefill` call of `toggle` (`af.label`)
//    11-Apr-2013 (CT) Add polymorphic attributes to attribute filter menu
//    29-Apr-2013 (CT) Use `$GTW.show_message`, not `console.error`
//     2-Mar-2014 (CT) Protect recursion in `attr_filters.add`
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    31-Oct-2014 (CT) Fix compatibility with jQuery 1.9 (attr vs. prop)
//    31-Oct-2014 (CT) Use pure buttons for QR-form;
//                     replace `fix_buttons` by `fix_button_state`
//    21-Nov-2014 (CT) Change `attr_select` to `hd_input`
//    21-Nov-2014 (CT) Change `config_button` button to just change visibility
//     2-Dec-2014 (CT) Change `direction` and `disabler` buttons to use
//                     `gtw_a_toggle_button_pure`; factor `setup_a_toggle`
//     2-Dec-2014 (CT) Change `attr_select.cb.apply` to update
//                     `attr_select_display`
//     2-Dec-2014 (CT) Add `return false` to `attr_select.cb.apply` and
//                     `order_by.cb.apply`
//     4-Dec-2014 (CT) Change `order_by.cb.apply` to test class of `icon$`,
//                     not `dir$`, against `fa_icons.icon_class`, not `ui_class`
//    13-Jan-2015 (CT) Simplify menu structure by removing nested `a.button`
//                     (jquery-ui 1.11 doesn't need the `a` anymore)
//    14-Jan-2015 (CT) Change `menu_select_cb` to be invoked by `select` event
//                     of `menu`
//                     + change signature of `add_attr_filter_cb`,
//                       `attr_select.cb.add`, `op_select_cb`, and
//                       `order_by.cb.add_criterion` from `(ev)`
//                       to `(item, choice)`
//    14-Jan-2015 (CT) Factor `hide_menu`
//    15-Jan-2015 (CT) Use `click` and `keydown`, not `focus`, to open dialogs
//                     + Pass `clear_callback` to `gtw_hd_input`
//    27-Mar-2015 (CT) Use `flipfit`, not `fit`, for `collision`
//    27-Mar-2015 (CT) Factor `serialized_form`, add `:checkbox:not(:checked)`
//    31-Mar-2015 (CT) Use `fit`, not `flipfit`, for `collision`
//                     (`flipfit` truncates on the left of completion info)
//    28-Apr-2015 (CT) Add guards for undefined `af_map [label]`
//                     to `attr_select` and`order_by`
//    20-Jan-2016 (CT) Use `$V5a.history_push`, not `$GTW.push_history`
//     3-May-2016 (CT) Add guard for `afs` to `setup_op_button`
//     3-May-2016 (CT) Save `form$` in scope of `gtw_query_restriction`
//                     + Bind `submit` of `form$` to `submit_cb`
//     4-May-2016 (CT) Change `attr_filters` to allow both `attrs` and
//                     `children_np` for the same filter
//    19-May-2016 (CT) Add guard for `typ.attrs` to `new_menu__add_sub_cnp`
//     8-Feb-2017 (CT) Support several `qr_form_buttons` in `submit_ajax_cb`
//    ««revision-date»»···
//--
( function ($, undefined) {
    "use strict";

    var L = $GTW.L;
    $.fn.gtw_query_restriction = function (qrs, opts) {
        var completer_position = $.extend
            ( { my         : "left top"
              , at         : "left bottom"
              }
            , opts && opts ["completer_position"] || {}
            );
        var dialog_position = $.extend
            ( { my         : "right top"
              , at         : "right bottom"
              }
            , opts && opts ["dialog_position"] || {}
            );
        var fa_icons = new $GTW.FA_Icon_Map
            (opts && opts ["fa_icon_map"] || {});
        var form$ = $(this);
        var menu_position  = $.extend
            ( { my         : "right top"
              , at         : "left bottom"
              , collision  : "fit"
              }
            , opts && opts ["menu_position"] || {}
            );
        var selectors = $.extend
            ( { ascending                : ".asc"
              , attr_filter_container    : "div.attr-filter"
              , attr_filter_disabler     : "a.disabler"
              , attr_filter_label        : "label"
              , attr_filter_op           : ".op.button"
              , attr_filter_value        : ":input.value"
              , attr_filter_value_entity : "span.value.Entity"
              , attr_select_attributes   : "ul.attributes"
              , attr_select_display      : ":input.value.display[id=QR-fields]"
              , attr_select_item         : "li"
              , attr_select_value        : ":input.value.hidden[name=fields]"
              , attrs_container          : "fieldset.attrs"
              , config_element           : ".config"
              , descending               : ".desc"
              , disabled_button          : "button[class=disabled]"
              , disabler                 : ".disabler"
              , head_line                : "h1.headline"
              , limit                    : ":input[name=limit]"
              , menu_item                : "li"
              , object_container         : "table.Object-List"
              , offset                   : ":input[name=offset]"
              , order_by_criteria        : "ul.attributes"
              , order_by_criterion       : "li"
              , order_by_direction       : ".direction"
              , order_by_display         : ":input.value.display[id=QR-order_by]"
              , order_by_value           : ":input.value.hidden[name=order_by]"
              , prototype                : "ul.prototype li"
              , qr_form_buttons          : ".QR > .buttons"
              , submit                   : "[type=submit]"
              }
            , fa_icons.selectors
            , opts && opts ["selectors"] || {}
            );
        var ui_class = $.extend
            ( { active_menu_button    : "active-menu-button"
              }
            , opts && opts ["ui_class"] || {}
            );
        var options  = $.extend
            ( { asf_closing_flag    : "gtw_asf_dialog_closing"
              , obf_closing_flag    : "gtw_obf_dialog_closing"
              , treshold            : 0
              }
            , opts || {}
            , { completer_position  : completer_position
              , dialog_position     : dialog_position
              , fa_icon_map         : fa_icons
              , menu_position       : menu_position
              , selectors           : selectors
              , ui_class            : ui_class
              }
            );
        var qr$    = $(this);
        var body$  = $("body").last ();
        var af_map = {};
        var as_widget$, ob_widget$;
        var attr_filters =
            ( function () {
                var result = [];
                var name_sep = new RegExp (qrs.name_sep, "g");
                var add = function add (filters, prefix, ui_prefix) {
                    for (var i = 0, li = filters.length, f; i < li; i++) {
                        f = filters [i];
                        if (prefix) {
                            f.key   = prefix    + qrs.name_sep + f.name;
                            f.label = ui_prefix + qrs.ui_sep   + f.ui_name;
                        } else {
                            f.key   = f.name;
                            f.label = f.ui_name;
                        };
                        f.q_name          = f.key.replace (name_sep, ".");
                        f.ops_selected    = [];
                        af_map [f.label]  = f;
                        af_map [f.q_name] = f;
                        result.push (f);
                        if ("attrs" in f && f.attrs) {
                            add (f.attrs, f.key, f.label);
                        };
                        if ("children_np" in f) {
                            for ( var j = 0, lj = f.children_np.length, c
                                ; j < lj
                                ; j++
                                ) {
                                c = f.children_np [j];
                                if ("attrs" in c && c.attrs) {
                                    add ( c.attrs
                                        , f.key   + "[" + c.type_name    + "]"
                                        , f.label + "[" + c.ui_type_name + "]"
                                        );
                                };
                            };
                        };
                    };
                };
                if (qrs.filters) {
                    add (qrs.filters);
                };
                return result;
              } ()
            );
        var op_map_by_sym =
            ( function () {
                var result = {}, k, v, label;
                for (k in qrs.op_map) {
                    if (qrs.op_map.hasOwnProperty (k)) {
                        v              = qrs.op_map [k];
                        v.key          = k;
                        // if label contains stuff like `&ge;` we need to
                        // run it through `html` because we'll later want
                        // to look up `but$.html ()` in `op_map_by_sym`
                        //     Can't use `L`, because that keeps html-quotes
                        label          = $("<a>").append (v.label).html ();
                        result [v.sym] = v;
                        result [label] = v;
                    };
                };
                return result;
              } ()
            );
        var sig_map =
            ( function () {
                var result = {}, k, v;
                for (k in qrs.sig_map) {
                    if (qrs.sig_map.hasOwnProperty (k)) {
                        v = qrs.sig_map [k];
                        result [k] = $.map
                            ( v
                            , function (value) {
                                return qrs.op_map [value];
                              }
                            );
                    };
                };
                return result;
              } ()
            );
        var toggle_disabled_state = function toggle_disabled_state (menu$, choice, state) {
            var S       = options.selectors;
            var cl      = choice.length;
            menu$.find (S.menu_item).each
                ( function () {
                    var a$         = $(this);
                    var c          = a$.data ("gtw_qr_choice");
                    var label      = c ? c.label : a$.html ();
                    var label_head = label.slice (0, cl);
                    var label_sep  = label [cl];
                    var match      =
                        (  (cl <= label.length)
                        && (!label_sep)
                        || (label_sep === "/")
                        );
                    if (match && (choice === label_head)) {
                        a$.toggleClass ("ui-state-disabled", state);
                    };
                  }
                );
        };
        var add_attr_filter_cb = function add_attr_filter_cb (item, choice) {
            var S       = options.selectors;
            var afs$    = $(S.attr_filter_container, qr$);
            var head$   = afs$.filter
                ( function () {
                    return $(this).prop ("title") <= choice.label;
                  }
                );
            var nf$ = new_attr_filter (choice);
            if (head$.length) {
                head$.last ().after  (nf$);
            } else if (afs$.length) {
                afs$.first ().before (nf$);
            } else {
                $(S.attrs_container).append (nf$);
            };
            setup_esf (nf$);
            // `focus` must be done after `setup_esf`
            $(S.attr_filter_value, nf$).focus ();
        };
        var adjust_op_menu = function adjust_op_menu (afs) {
            var S       = options.selectors;
            var menu$   = afs.ops_menu$;
            menu$.element.find (S.menu_item).each
                ( function () {
                    var a$    = $(this);
                    var label = a$.html ();
                    var map   = afs.ops_selected;
                    var op    = op_map_by_sym [label];
                    if (op) {
                        a$.toggleClass ("ui-state-disabled", !! map [op.sym]);
                    };
                  }
                );
        };
        var attach_menu = function attach_menu (but$, menu) {
            but$.click (menu_click_cb)
                .data  ("gtw_qr_menu$", menu);
        };
        var attr_select =
            { cb              :
                { add         : function add (item, choice) {
                      var S       = options.selectors;
                      var label   = choice.label;
                      var c$      = attr_select.new_attr (label);
                      var but$    = as_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      as_widget$.find    (S.attr_select_attributes).append (c$);
                      attr_select.toggle (menu$, label, true);
                      as_widget$.find    (S.apply_button).focus ();
                  }
                , apply       : function apply (ev) {
                      var S      = options.selectors;
                      var attrs$ = as_widget$.find
                          (S.attr_select_attributes + " " + S.attr_select_item);
                      var labels = [];
                      var values = [];
                      attrs$.each
                          ( function () {
                                var a$ = $(this);
                                var v$ = a$.find ("b");
                                if (! a$.hasClass ("disabled")) {
                                    var label = v$.html ();
                                    if (label) {
                                        var af    = af_map [label];
                                        var name  = (af === undefined) ?
                                                label : af.q_name;
                                        labels.push (label);
                                        values.push (name);
                                    };
                                };
                            }
                          )
                      $(S.attr_select_display).val (labels.join (", "));
                      $(S.attr_select_value).val   (values.join (", "));
                      attr_select.cb.close ();
                      qr$.find (S.apply_button).focus ();
                      return false;
                  }
                , clear       : function clear (ev, ui) {
                      var S = options.selectors;
                      var but$    = as_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      as_widget$.find (S.attr_select_attributes).empty ();
                      menu$.find (S.menu_item).removeClass ("ui-state-disabled");
                  }
                , close       : function close (ev) {
                      as_widget$.dialog ("close");
                      attr_select.cb.clear ();
                  }
                , disabler    : function disabler (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var attr$    = target$.closest (S.attr_select_item);
                      var but$     = as_widget$.find (S.add_button);
                      var menu$    = but$.data       ("gtw_qr_menu$").element;
                      var choice   = attr$.find      ("b").html ();
                      var disabled = attr$.hasClass  ("disabled");
                      var title    = disabled ?
                          options.title.disabler : options.title.enabler;
                      attr$.toggleClass  ("disabled",   !disabled);
                      attr_select.toggle (menu$, choice, disabled);
                      target$.prop       ("title", title);
                      return false;
                  }
                , open        : function open (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var value$  = $(S.attr_select_value);
                      var val     = value$.val ();
                      var width   = qr$.width  ();
                      var dialog;
                      if (as_widget$ == null) {
                          as_widget$ = attr_select.setup_widget (target$);
                      };
                      attr_select.cb.clear ();
                      attr_select.prefill  (val ? val.split (",") : []);
                      as_widget$
                          .dialog
                              ( "option"
                              , { dialogClass : "no-close"
                                , width       : "auto"
                                }
                              )
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( $.extend
                                      ( {}
                                      , options.dialog_position
                                      , { of : target$ }
                                      )
                                  );
                  }
                }
            , new_attr          : function new_attr (label) {
                  var S      = options.selectors;
                  var result = as_widget$.find (S.prototype).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  result.find (S.disabler)
                      .each   (setup_disabler)
                      .click  (attr_select.cb.disabler);
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = options.selectors;
                  var attrs$  = as_widget$.find (S.attr_select_attributes);
                  var but$    = as_widget$.find (S.add_button);
                  var menu$   = but$.data ("gtw_qr_menu$").element;
                  var af, a$, label;
                  for (var i = 0, li = choices.length, choice; i < li; i++) {
                      choice = $.trim (choices [i]);
                      if (choice.length) {
                          af    = af_map [choice];
                          label = (af === undefined) ? choice : af.label;
                          a$    = attr_select.new_attr (label);
                          attrs$.append (a$);
                          attr_select.toggle (menu$, label, true);
                      };
                  };
              }
            , setup             : function setup () {
                  var p$ = $(this).parent ();
                  attr_select.hd_input$ = p$;
                  p$.gtw_hd_input
                      ( { callback       : attr_select.cb.open
                        , clear_callback : attr_select.cb.clear
                        , closing_flag   : options.asf_closing_flag
                        , trigger_event  : "click keydown"
                        }
                      );
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = options.selectors;
                  var saf$   = options ["attr_select_form_html"];
                  var result, saf;
                  if (! saf$) {
                      $.gtw_ajax_2json
                          ( { async       : false
                            , success     : function (response, status) {
                                if (! response ["error"]) {
                                    if ("html" in response) {
                                        saf = response.html;
                                    } else {
                                        $GTW.show_message
                                            ("Ajax Error", response);
                                    };
                                } else {
                                  $GTW.show_message
                                      ("Ajax Error", response.error);
                                }
                              }
                            , url         : options.url.qx_asf
                            }
                          );
                      if (! saf) {
                          return;
                      };
                      saf$ = $(saf);
                      options.attr_select_form_html = saf$;
                  };
                  result   = saf$.dialog
                      ( { dialogClass : "no-close"
                        , autoOpen    : false
                        , title       : saf$.prop ("title")
                        , width       : "auto"
                        }
                      );
                  result.find (S.prototype)
                      .prop ("title", options.title.attr_select_sortable);
                  result.find (S.attr_select_attributes).sortable
                      ( { close       : attr_select.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_button_pure ({icon_map : fa_icons});
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu_nested
                                    (qrs.filters, attr_select.cb.add)
                                );
                            }
                          );
                  result.find (S.apply_button).click  (attr_select.cb.apply);
                  result.find (S.cancel_button).click (attr_select.cb.close);
                  result.find (S.clear_button).click  (attr_select.cb.clear);
                  return result;
              }
            , toggle         : toggle_disabled_state
            };
        var config_button_cb = function config_button_cb (ev) {
            var S      = options.selectors;
            var but$   = $(ev.target);
            var cfg$   = $(S.config_element);
            cfg$.toggleClass ("hidden");
            but$.toggleClass ("pure-button-active");
        };
        var disabler_cb = function disabler_cb (ev) {
            var S        = options.selectors;
            var afc$     = $(ev.target).closest (S.attr_filter_container);
            var dis$     = $(S.attr_filter_disabler, afc$);
            var val$     = $(S.attr_filter_value,    afc$);
            var disabled = val$.prop ("disabled");
            var title    = disabled ?
                options.title.disabler : options.title.enabler;
            afc$.toggleClass ("ui-state-disabled", !disabled);
            dis$.prop        ("title",             title);
            val$.prop        ("disabled",          !disabled);
            return false;
        };
        var fix_button_state = function fix_button_state
                (sel, context, state) {
            var but$   = $(sel, context);
            var method = state ? "enable" : "disable";
            but$.gtw_button_pure (method);
        };
        var hide_menu = function hide_menu (menu$) {
            var amb$ = $("." + options.ui_class.active_menu_button);
            amb$.removeClass (options.ui_class.active_menu_button);
            menu$.hide ();
        };
        var hide_menu_cb = function hide_menu_cb (ev) {
            var menu$ = $(".drop-menu:visible");
            if (menu$.length) {
                var target$ = $(ev.target);
                var esc_p   = ev.keyCode === $.ui.keyCode.ESCAPE;
                var tc      = target$.closest (".drop-menu");
                if (esc_p || ! tc.length) {
                    hide_menu (menu$);
                };
            };
        };
        var menu_click_cb = function menu_click_cb (ev) {
            var but$ = $(ev.delegateTarget);
            var menu = but$.data ("gtw_qr_menu$");
            var opts = menu.element.data ("gtw_qr_options");
            if (menu.element.is (":visible")) {
                hide_menu (menu.element);
            } else {
                hide_menu_cb (ev); // hide other open menus, if any
                if (opts && "open" in opts) {
                    opts.open (ev, menu);
                };
                menu.element
                    .show ()
                    .position
                      ( $.extend
                          ( options.menu_position
                          , opts && opts ["position"] || {}
                          , { of : but$ }
                          )
                      )
                      // XXX zIndex deprecated in jQueryUI 1.11
                      // http://jqueryui.com/upgrade-guide/1.11/#deprecated-zindex
                    .zIndex (but$.zIndex () + 1)
                    .focus  ();
                but$.addClass (options.ui_class.active_menu_button);
                if (ev && "stopPropagation" in ev) {
                    ev.stopPropagation ();
                };
            };
        };
        var menu_select_cb = function menu_select_cb (ev, ui) {
            var item    = ui.item;
            var cb      = item.data    ("gtw_qr_callback");
            var choice  = item.data    ("gtw_qr_choice");
            var menu$   = item.closest (".cmd-menu");
            cb (item, choice);
            hide_menu (menu$);
        };
        var new_attr_filter = function new_attr_filter (choice) {
            var S = options.selectors;
            var op  = op_map_by_sym ["=="] ; // last-op ???
            var key = choice.key + qrs.op_sep + op.key;
            var ajx = false;
            if (! ("attr_filter_html" in choice)) {
                $.gtw_ajax_2json
                    ( { async       : false
                      , data        :
                          { key     : key
                          }
                      , success     : function (response, status) {
                            if (! response ["error"]) {
                                if ("html" in response) {
                                  choice.attr_filter_html = $(response.html);
                                  choice.attr_filter_html
                                      .find (S.attr_filter_disabler)
                                          .each (setup_disabler);
                                  ajx = true;
                                } else {
                                  $GTW.show_message ("Ajax Error", response);
                                }
                            } else {
                                $GTW.show_message
                                    ("Ajax Error", response.error);
                            };
                        }
                      , url         : options.url.qx_af_html
                      }
                    , "Attribute filter"
                    );
                if (!ajx) {
                  return;
                };
            };
            var result = choice.attr_filter_html
                .clone (true)
                .data ("gtw_qr_choice", choice);
            update_attr_filter_op (result, op, key);
            $(S.attr_filter_op, result).each (setup_op_button);
            return result;
        };
        var new_menu__add = function new_menu__add (choice, menu, cb, off) {
            var S      = options.selectors;
            var label  = choice.label.substr (off || 0);
            var result = $(L ("li", { html : label }));
            result.data ({ gtw_qr_callback : cb, gtw_qr_choice : choice});
            menu.append (result);
            return result;
        };
        var new_menu__add_nested = function new_menu__add_nested (choice, menu, cb, off, pred, icnp) {
            var S      = options.selectors;
            var label  = choice.label.substr (off || 0);
            var offs   = choice.label.length + qrs.ui_sep.length;
            var sub, tail = "", treshold = 2;
            if (pred (choice)) {
                new_menu__add (choice, menu, cb, off);
                tail     = "/...";
                treshold = 3;
            };
            if ("attrs" in choice) {
                if (choice.attrs.length > treshold) {
                    sub = $(L ("li", { html : label + tail }));
                    menu.append (sub);
                    new_menu__add_sub (choice.attrs, sub, cb, offs, pred, icnp);
                } else {
                    for (var j = 0, lj = choice.attrs.length; j < lj; j++) {
                        new_menu__add_nested
                            (choice.attrs [j], menu, cb, off, pred, icnp);
                    };
                };
            } else if (icnp && "children_np" in choice) {
                sub = $(L ("li", { html : label + tail }));
                menu.append (sub);
                new_menu__add_sub_cnp (choice.children_np, sub, cb, offs, pred);
            };
        };
        var new_menu__add_sub = function new_menu__add_sub (choices, menu, cb, off, pred, icnp) {
            var sub_menu = $(L ("ul"));
            menu.append (sub_menu);
            for (var i = 0, li = choices.length; i < li; i++) {
                new_menu__add_nested
                    (choices [i], sub_menu, cb, off, pred, icnp);
            };
        };
        var new_menu__add_sub_cnp = function new_menu__add_sub_cnp (children_np, menu, cb, off, pred) {
            var S        = options.selectors;
            var sub_menu = $(L ("ul"));
            var etn, offs, typ_menu, typ;
            menu.append (sub_menu);
            for (var i = 0, li = children_np.length; i < li; i++) {
                typ  = children_np [i];
                if (typ.attrs) {
                    etn  = "[" + typ.ui_type_name + "]";
                    offs = off + etn.length;
                    typ_menu = $(L ("li", { html : etn }));
                    sub_menu.append (typ_menu);
                    new_menu__add_sub
                        (typ.attrs, typ_menu, cb, offs, pred, true);
                };
            };
        };
        var new_menu__create = function new_menu__create (options) {
            var result = $(L ("ul.drop-menu.cmd-menu"));
            result.data ({ gtw_qr_options : options });
            return result;
        };
        var new_menu__finish = function new_menu__finish (menu) {
            var result = menu
                .menu     ({ select : menu_select_cb })
                .appendTo (body$)
                .css      ({ top: 0, left: 0, position : "absolute" })
                .hide     ()
                .data     ("ui-menu");
            return result;
        };
        var new_menu = function new_menu (choices, cb, kw) {
            var opts = (kw && "opts" in kw) ? kw.opts : {};
            var menu = new_menu__create (opts);
            for (var i = 0, li = choices.length; i < li; i++) {
                new_menu__add (choices [i], menu, cb, 0);
            };
            return new_menu__finish (menu);
        };
        var new_menu_nested = function new_menu_nested (choices, cb, kw) {
            var pred = (kw && "pred" in kw) ? kw.pred
                         : function () { return true; };
            var icnp = (kw && "icnp" in kw) ? kw.icnp : false;
            var opts = (kw && "opts" in kw) ? kw.opts : {};
            var menu = new_menu__create (opts);
            menu.addClass ("nested");
            for (var i = 0, li = choices.length; i < li; i++) {
                new_menu__add_nested (choices [i], menu, cb, 0, pred, icnp);
            };
            return new_menu__finish (menu);
        };
        var op_select_cb = function op_select_cb (item, choice) {
            var S       = options.selectors;
            var but$    = $("." + options.ui_class.active_menu_button).first ();
            var afc$    = but$.closest (S.attr_filter_container);
            var val$    = $(S.attr_filter_value, afc$);
            var name    = val$.prop ("name");
            var prefix  = name.split  (qrs.op_sep) [0];
            var key     = prefix + qrs.op_sep + choice.key;
            update_attr_filter_op (afc$, choice, key);
            setTimeout
                ( function () {
                    $(S.attr_filter_value, afc$).focus ();
                  }
                , 1
                );
        };
        var order_by =
            { cb              :
                { add_criterion : function add_criterion (item, choice) {
                      var S       = options.selectors;
                      var label   = choice.label;
                      var c$      = order_by.new_criterion (label);
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      ob_widget$.find (S.order_by_criteria).append (c$);
                      order_by.toggle_criteria (menu$, label, true);
                      ob_widget$.find (S.apply_button).focus ();
                  }
                , apply         : function apply (ev) {
                      var S     = options.selectors;
                      var crit$ = ob_widget$.find
                          (S.order_by_criteria + " " + S.order_by_criterion);
                      var labels = [];
                      var values = [];
                      crit$.each
                          ( function () {
                                var c$ = $(this);
                                var v$ = c$.find ("b");
                                if (! c$.hasClass ("disabled")) {
                                    var dir$  = c$.find (S.order_by_direction);
                                    var icon$ = $(".fa", dir$);
                                    var label = v$.html ();
                                    if (label) {
                                        var desc  = icon$.hasClass
                                            (fa_icons.icon_class.SORT_DESC);
                                        var sign  = desc ? "-" : "";
                                        var af    = af_map [label];
                                        var name  = (af === undefined) ?
                                                label : af.q_name;
                                        labels.push (sign + label);
                                        values.push (sign + name);
                                    };
                                };
                            }
                          )
                      $(S.order_by_display).val (labels.join (", "));
                      $(S.order_by_value)  .val (values.join (", "));
                      ob_widget$.dialog ("close");
                      qr$.find (S.apply_button).focus ();
                      return false;
                  }
                , before_close  : function before_close (ev) {
                      var hdi$ = order_by.hd_input$;
                      if (hdi$) {
                          hdi$.data (options.obf_closing_flag, true);
                      };
                  }
                , clear         : function clear (ev, ui) {
                      var S = options.selectors;
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      ob_widget$.find (S.order_by_criteria).empty ();
                      menu$.find (S.menu_item).removeClass ("ui-state-disabled");
                  }
                , close         : function close (ev) {
                      var hdi$ = order_by.hd_input$;
                      if (hdi$) {
                          hdi$.removeData (options.obf_closing_flag);
                      };
                  }
                , dir           : function dir (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var dir$     = crit$.find      (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  }
                , disabler      : function disabler (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var but$     = ob_widget$.find (S.add_button);
                      var menu$    = but$.data       ("gtw_qr_menu$").element;
                      var choice   = crit$.find      ("b").html ();
                      var disabled = crit$.hasClass  ("disabled");
                      var title    = disabled ?
                          options.title.disabler : options.title.enabler;
                      crit$.toggleClass        ("disabled",   !disabled);
                      order_by.toggle_criteria (menu$, choice, disabled);
                      target$.prop             ("title", title);
                      return false;
                  }
                , open          : function open (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var obw$    = ob_widget$;
                      var width   = qr$.width ();
                      var dialog;
                      if (obw$ == null) {
                          ob_widget$ = obw$ = order_by.setup_widget (target$);
                      };
                      order_by.cb.clear ();
                      order_by.prefill  (target$.val ().split (","));
                      obw$.dialog ("option", "width", "auto")
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( $.extend
                                      ( {}
                                      , options.dialog_position
                                      , { of : target$ }
                                      )
                                  );
                  }
                }
            , new_criterion     : function new_criterion (label, desc) {
                  var S      = options.selectors;
                  var result = ob_widget$.find (S.prototype).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  result.find (S.order_by_direction)
                      .each   (order_by.setup_dir)
                      .click  (order_by.cb.dir);
                  result.find (S.disabler)
                      .each   (setup_disabler)
                      .click  (order_by.cb.disabler);
                  if (desc) {
                      dir$ = result.find (S.order_by_direction);
                      dir$.gtw_a_toggle_button_pure ("toggle");
                      order_by.toggle_dir           (dir$);
                  };
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = options.selectors;
                  var crits$  = ob_widget$.find (S.order_by_criteria);
                  var but$    = ob_widget$.find (S.add_button);
                  var menu$   = but$.data ("gtw_qr_menu$").element;
                  var c$, desc;
                  for (var i = 0, li = choices.length, choice; i < li; i++) {
                      choice = $.trim (choices [i]);
                      if (choice.length) {
                          desc = false;
                          if (choice [0] === "-") {
                              desc = true;
                              choice = choice.slice (1);
                          }
                          c$ = order_by.new_criterion (choice, desc);
                          crits$.append (c$);
                          order_by.toggle_criteria (menu$, choice, true);
                      };
                  };
              }
            , setup             : function setup () {
                  var p$ = $(this).parent ();
                  order_by.hd_input$ = p$;
                  p$.gtw_hd_input
                      ( { callback       : order_by.cb.open
                        , clear_callback : order_by.cb.clear
                        , closing_flag   : options.obf_closing_flag
                        , trigger_event  : "click keydown"
                        }
                      );
              }
            , setup_dir         : function setup_dir () {
                  setup_a_toggle
                      ( $(this)
                      , options.title.order_by_asc
                      , { "alt-name" : "SORT_DESC", name : "SORT_ASC" }
                      );
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = options.selectors;
                  var obf$   = options ["order_by_form_html"];
                  var result;
                  if (! obf$) {
                      $.gtw_ajax_2json
                          ( { async       : false
                            , success     : function (response, status) {
                                if (! response ["error"]) {
                                    if ("html" in response) {
                                        obf$ = $(response.html);
                                        options.order_by_form_html = obf$;
                                    } else {
                                        $GTW.show_message
                                            ("Ajax Error", response);
                                    };
                                } else {
                                  $GTW.show_message
                                      ("Ajax Error", response.error);
                                }
                              }
                            , url         : options.url.qx_obf
                            }
                          );
                      if (! obf$) {
                          return;
                      };
                  };
                  result = obf$.dialog
                      ( { autoOpen    : false
                        , beforeClose : order_by.cb.before_close
                        , close       : order_by.cb.close
                        , title       : obf$.prop ("title")
                        }
                      );
                  result.find (S.prototype)
                      .prop ("title", options.title.order_by_sortable);
                  result.find (S.order_by_criteria).sortable
                      ( { close       : order_by.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_button_pure ({icon_map : fa_icons});
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu_nested
                                    (qrs.filters, order_by.cb.add_criterion)
                                );
                            }
                          );
                  result.find (S.apply_button).click  (order_by.cb.apply);
                  result.find (S.cancel_button).click
                    ( function () {
                          return ob_widget$.dialog ("close");
                      }
                    );
                  result.find (S.clear_button).click  (order_by.cb.clear);
                  return result;
              }
            , toggle_criteria   : toggle_disabled_state
            , toggle_dir        : function toggle_dir (dir$) {
                  var icon$ = $(".fa", dir$);
                  var asc   = icon$.hasClass (fa_icons.icon_class.SORT_ASC);
                  var title = asc ?
                      options.title.order_by_asc : options.title.order_by_desc;
                  dir$.prop ("title", title);
              }
            };
        var serialized_form = function serialized_form (form$, button) {
            var result = [form$.serialize ()];
            var unchecked$ = $(":checkbox", form$).filter (":not(:checked)");
            if (button) {
                result.push (button.name + "=" + button.value);
            };
            unchecked$.each
                ( function () {
                    // unchecked checkboxes aren't submitted by HTML forms
                    result.push (this.name + "=" + "no");
                  }
                );
            return result.join ("&");
        };
        var setup_a_toggle = function setup_a_toggle (a$, title, names, cb) {
            var opts = { click_handler : cb, icon_map : fa_icons };
            a$.data                     (names)
              .append                   ($(L ("i.fa")))
              .gtw_a_toggle_button_pure (opts)
              .prop                     ("title", title);
        };
        var setup_config = function setup_config () {
            var S      = options.selectors;
            var but$   = $(this);
            var cfg$   = $(S.config_element);
            but$.click (config_button_cb);
            if (! cfg$.hasClass ("hidden")) {
                but$.toggleClass ("pure-button-active");
            };
        };
        var setup_disabler = function setup_disabler () {
            setup_a_toggle
                ( $(this)
                , options.title.disabler
                , { "alt-name" : "ENABLE", name : "DISABLE" }
                );
        };
        var setup_esf = function setup_esf (context) {
            var S = options.selectors;
            $(S.attr_filter_value_entity, context).gtw_e_type_selector_hd
                (options);
        };
        var setup_op_button = function setup_op_button () {
            var but$   = $(this);
            var afc$   = but$.closest (options.selectors.attr_filter_container);
            var afs    = af_map [afc$.prop ("title")];
            var label  = but$.html ();
            var op     = op_map_by_sym [label];
            if (afs) {
                if (! ("ops_menu$" in afs)) {
                    afs.ops_menu$ = new_menu
                        ( sig_map [afs.sig_key]
                        , op_select_cb
                        , { opts :
                              { open     : function (ev, menu) {
                                    adjust_op_menu (afs);
                                }
                              , position : { my : "left top" }
                              }
                          }
                        );
                };
                attach_menu (but$, afs.ops_menu$);
                afs.ops_selected [op.sym] = true;
            };
        };
        var submit_ajax_cb = function submit_ajax_cb (response) {
            var S    = options.selectors;
            var qfb$ = $(S.qr_form_buttons);
            var p;
            if ("object_container" in response) {
                $(S.object_container).last ().replaceWith
                    (response.object_container);
            };
            if ("head_line" in response) {
                $(S.head_line).html (response.head_line);
            };
            if ("limit" in response) {
                $(S.limit).val (response.limit);
            };
            if ("offset" in response) {
                $(S.offset).val (response.offset);
            };
            if ("qr_next_p" in response) {
                p = response.qr_next_p;
                qfb$.each
                    ( function () {
                        fix_button_state (S.next_button,  this, p);
                        fix_button_state (S.last_button,  this, p);
                      }
                    );
            };
            if ("qr_prev_p" in response) {
                p = response.qr_prev_p;
                qfb$.each
                    ( function () {
                        fix_button_state (S.first_button, this, p);
                        fix_button_state (S.prev_button , this, p);
                      }
                    );
            };
            if ("callbacks" in response) {
                for ( var i = 0, li = response.callbacks.length, cb, cbn
                    ; i < li
                    ; i++
                    ) {
                    cbn = response.callbacks [i];
                    cb  = options.callback [cbn];
                    if (cb) {
                        cb ();
                    };
                };
            };
            $V5a.history_push
                (qr$.prop ("action") + "?" + serialized_form (qr$));
        };
        var submit_cb = function submit_cb (ev) {
            var args = serialized_form (form$, this);
            $.getJSON (form$.prop ("action"), args, submit_ajax_cb);
            return false;
        };
        var tr_selector = function tr_selector (label) {
            var head = options.selectors.attr_filter_container, tail;
            if (label.length) {
                tail = "[title^='"+label+"']";
            } else {
                tail = "[title]";
            };
            return head + tail;
        };
        var update_attr_filter_op = function update_attr_filter_op (afc$, op, key) {
            var S     = options.selectors;
            var afm   = af_map;
            var title = afc$.prop ("title");
            var afs   = afm [title];
            var but$  = $(S.attr_filter_op, afc$);
            var oop   = op_map_by_sym [but$.html ()];
            if (oop) {
                afs.ops_selected [oop.sym] = false;
            };
            $(S.attr_filter_label, afc$).prop ("for", key);
            $(S.attr_filter_value, afc$)
                .not (".hidden")
                    .prop ("id", key)
                    .end ()
                .not (".display")
                    .prop ("name", key);
            $(S.attr_filter_op,    afc$)
                .prop ("title", op.desc)
                .html (op.label);
            afs.ops_selected [op.sym] = true;
        };
        options.esf_focusee = qr$.find (selectors.apply_button);
        $(document).bind ("click.menuhide keyup.menuhide", hide_menu_cb);
        $(selectors.button).gtw_button_pure ({icon_map : fa_icons});
        $(selectors.add_button, qr$)
            .each
                ( function () {
                    attach_menu
                        ( $(this)
                        , new_menu_nested
                            ( qrs.filters, add_attr_filter_cb
                            , { pred : function (choice) {
                                    return "sig_key" in choice;
                                }
                              , icnp : true
                              }
                            )
                        );
                  }
                );
        $(selectors.attrs_container)
            .find (selectors.attr_filter_op)
                .each (setup_op_button)
                .end  ()
            .find (selectors.attr_filter_disabler)
                .each (setup_disabler)
                .end  ();
        setup_esf ();
        $(selectors.attrs_container)
            .delegate (selectors.attr_filter_disabler, "click", disabler_cb);
        $(selectors.order_by_display).each    (order_by.setup);
        $(selectors.attr_select_display).each (attr_select.setup);
        $(selectors.config_button).each       (setup_config);
        qr$.delegate (selectors.submit, "click", submit_cb);
        form$.submit (submit_cb);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
