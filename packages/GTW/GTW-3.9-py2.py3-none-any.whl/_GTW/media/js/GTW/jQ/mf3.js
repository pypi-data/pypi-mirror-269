// Copyright (C) 2014-2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/mf3.js
//
// Purpose
//    jQuery plugin for MF3-forms
//
// Revision Dates
//    28-Apr-2014 (CT) Creation
//     3-May-2014 (CT) Ignore `input` elements with class `readonly`
//     9-May-2014 (CT) Add `completer`
//    10-May-2014 (CT) Change `completer.get_values` to use `cargo.field_values`
//    13-May-2014 (CT) Fix typos; bind `field_change_cb` after `completer.setup`
//    13-May-2014 (CT) Add argument `cargo` tp `completer.put_values`
//    14-May-2014 (CT) Change `completer.get_completions.success_cb` to
//                     handle `feedback`
//    15-May-2014 (CT) Factor `field_type` (`.checkbox`, `.id_ref`, `.normal`)
//    16-May-2014 (CT) Add support for `.Entity-Field .Display`
//    16-May-2014 (CT) Add `action_callback`
//    18-Jun-2014 (CT) Add `action_callback.add_rev_ref`;
//                     factor `setup_sub_form`
//    19-Jun-2014 (CT) Add `action_callback.remove`; DRY `setup_sub_form`
//    19-Jun-2014 (CT) Change `action_callback.close` to set `display` <input>
//     2-Jul-2014 (CT) Add `form_errors`
//     8-Jul-2014 (CT) Add `form_pid` to AJAX requests
//     8-Jul-2014 (CT) Add `return false` to callback function `add_rev_ref`
//    24-Aug-2014 (CT) Pass `pid`, `sid`, `sigs` to `gtw_e_type_selector_hd_mf3`
//    26-Aug-2014 (CT) Factor `close_section`, add `focus` to `close_section`
//    26-Aug-2014 (CT) Add `response.finished` to `completer.select_cb`
//    26-Aug-2014 (CT) Add `anchor` to `completer.completed_cb`
//    27-Aug-2014 (CT) Add `field_blur_cb` and `field_focus_cb`
//    28-Aug-2014 (CT) Add `composite_field` to `field_blur_cb`,
//                     `field_focus_cb`
//    29-Aug-2014 (CT) Add support for `max-rev-ref`
//    30-Aug-2014 (CT) Add guard for `ft` to `completer.put_values`
//    30-Aug-2014 (CT) Add `hide` and `show` calls for `$(S.form_errors)`
//     3-Sep-2014 (CT) Use `.call`, not `.apply`, in `entity_display_open_cb`
//    25-Sep-2014 (CT) Add `polish_field`
//    12-Dec-2014 (CT) Add `F_ACT` to `submit_cb`
//    15-Jan-2015 (CT) Factor key handling to `gtw_hd_input`,
//                     remove `entity_display_open_cb`
//    27-Feb-2015 (CT) Change `close_section` to call `focus` only once
//    24-Mar-2015 (CT) Move `removeClass ("open")` from `field_blur_cb` to
//                     `field_focus_cb` (avoid disruption of button click by
//                     page shift due to hiding of previously open `aside`)
//    27-Mar-2015 (CT) Pass `collision : flipfit` to `gtw_autocomplete`
//    31-Mar-2015 (CT) Use `fit`, not `flipfit`, for `collision`
//                     (`flipfit` truncates on the left of completion info)
//     2-Apr-2015 (CT) Add guard for `item.disabled` to `completer.select_cb`
//     3-Apr-2015 (CT) Add `field_type.id_ref_select`
//                     + add optional arg `ft` to `field_type.normal.reset`
//    14-Apr-2015 (CT) Use `response ["entity_p"]` in `completer.select_cb`,
//                     not `f_completer ["entity_p"]`
//    29-Apr-2015 (CT) Add `aside .error-msg` to `form_errors`
//    29-Apr-2015 (CT) Change `form_errors.display` to focus on first entry
//                     field with error
//    12-May-2015 (CT) Change `selectors.status` to `b` [used to be `b.Status`]
//    12-May-2015 (CT) Add `need_blur` to fix `polisher` breaking `completer`
//     1-Jun-2015 (CT) Add `remove_undo`, adapt `action_callback.remove`
//    31-Jul-2015 (CT) Change `polish_field` to handle `feedback`
//    21-Dec-2015 (CT) Add `action_callback.more_aside`
//    21-Dec-2015 (CT) Add `show_field_desc_cb`
//                     + remove `aside` from `field_focus_cb`
//    22-Dec-2015 (CT) Fix `action_callback.add_rev_ref` `add_rev_ref` hiding
//    23-Dec-2015 (CT) Factor `toggle_add_rev_ref` to DRY and fix
//                     `max_rev_ref` handling
//    26-Apr-2016 (CT) Use `form_spec.buddies`
//    14-Oct-2016 (CT) Change `clear` and `restore` to include `display_id_ref`
//    14-Oct-2016 (CT) Change `field_type.id_ref.put_input` to clear `edit`
//                     fields instead of setting `edit` to `undefined`
//                     + Ditto for `field_type.id_ref_select.put_input`
//    18-Oct-2016 (CT) Add `open4move`
//                     + Change `setup_entity_display` to use `data-action` for
//                       callback
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var L      = $GTW.L;

    var bwrap  = function bwrap (v) {
        return "<b>" + v + "</b>";
    };

    $.fn.gtw_mf3_form = function gtw_mf3_form (form_spec, opts) {
        var field_map = {};
        var selectors = $.extend
            ( { closable                 : "section"
              , composite_field          : ".Field-Composite"
              , container                : "div.Field"
              , container_rev_ref        : ".Field-Entity"
              , display_field            : ".Field.Display"
              , display_id_ref           : ".value.display.id_ref"
              , entity_list              : ".Entity-List"
              , err_msg                  : "div.error-msg"
              , field_desc               : "aside.Desc"
              , field_expl               : ".Expl"
              , form_element             : "form[id]"
              , form_errors              : "div.form-errors"
              , focusables               :
                  ".Field :input[id]:not(:hidden):not(.prefilled):not(.readonly)"
              , hidden_id_ref            : ".value.hidden.id_ref"
              , id_field                 : ".Field :input[id]"
              , input_field              :
                  ".Field :input[id]:not(.prefilled):not(.readonly)"
              , label_with_desc          : "label.desc-p"
              , status                   : "b"
              , submit                   : "[type=submit]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options   = $.extend
            ( { pre_submit_callbacks : []
              , form_spec            : form_spec
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        var closest_el_id = function closest_el_id (self, selector) {
            var closest$ = $(self).closest (selector);
            return closest$.prop ("id");
        };
        var action_callback =
            { add_rev_ref : function add_rev_ref (ev) {
                var S          = options.selectors;
                var a$         = $(this);
                var c$         = a$.closest (S.entity_list);
                var form_spec  = options.form_spec;
                var cargo      = form_spec.cargo;
                var F_id       = c$.prop ("id");
                var data       =
                    { form_pid        : cargo.pid
                    , sid             : cargo.sid
                    , sigs            : cargo.sigs
                    , trigger         : F_id
                    };
                var success_cb = function success_cb (answer, status, xhr) {
                    var new$;
                    if (! answer ["error"]) {
                        var fsu    = answer ["form_spec_update"];
                        var html   = answer ["html"];
                        c$.append (html);
                        $GTW.inspect.update_transitive (form_spec, fsu);
                        new$ = c$.children ().last ();
                        setup_sub_form     (new$);
                        toggle_add_rev_ref (c$);
                    } else {
                        $GTW.show_message
                            ("Ajax completion error: ", answer.error);
                    };
                };
                var url        = options.url.add_rev_ref;
                $.gtw_ajax_2json
                    ( { async         : true
                      , data          : data
                      , success       : success_cb
                      , url           : url
                      }
                    , "Add Rev_Ref"
                    );
                return false;
              }
            , clear : function clear (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                var d$    = $(S.display_id_ref, c$).first ();
                var ft    = d$.data ("field_type");
                if (ft) {
                    ft.clear (d$);
                };
                $(S.input_field, c$).each
                    ( function (n) {
                        var f$ = $(this);
                        var ft = f$.data ("field_type");
                        ft.clear (f$);
                      }
                    );
                $(S.focusables, c$).first ().focus ();
                return false;
              }
            , close : function close (ev) {
                close_section ($(this));
                return false;
              }
            , more_aside : function more_aside (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var x$    = a$.next (S.field_expl);
                x$.toggle ();
              }
            , open : function open (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                c$.removeClass ("closed");
                $(S.focusables, c$).first ().focus ();
                return false;
              }
            , open4move : function open4move (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                var d$    = $(S.display_id_ref, c$).first ();
                var ft    = d$.data ("field_type");
                if (ft) {
                    ft.clear (d$);
                };
                c$.removeClass ("closed");
                $(S.focusables, c$).first ().focus ();
                return false;
              }
            , remove : function remove (ev) {
                var S            = options.selectors;
                var a$           = $(this);
                var c$           = a$.closest (S.closable);
                var p$           = c$.closest (S.entity_list);
                var d$           = $(S.display_id_ref, c$).first ();
                var i$           = $(S.hidden_id_ref,  c$).first ();
                var elem_pid     = i$.val ();
                var form_spec    = options.form_spec;
                var cargo        = form_spec.cargo;
                var remove_cache = { vals : {}, sigs : {}};
                var f_values     = cargo.field_values;
                var sigs         = cargo.sigs;
                var F_id         = d$.prop ("id");
                var url          = options.url.remove;
                var cleanup_one  = function cleanup_one (id) {
                    remove_cache.vals [id] = f_values [id];
                    remove_cache.sigs [id] = sigs     [id];
                    delete f_values [id];
                    delete sigs     [id];
                };
                var cleanup    = function cleanup (answer) {
                    var feedback, undo_p;
                    cleanup_one (elem_pid);
                    $(":input[id]", c$).each
                        ( function (n) {
                            var f$   = $(this);
                            var F_id = f$.prop ("id");
                            cleanup_one (F_id);
                          }
                        );
                    if (answer) {
                        undo_p   = "undo" in answer;
                        feedback =
                            ( "<p class=\"feedback\">"
                            + ( undo_p
                                  ? ( "<a class=\"pure-button\""
                                    +   " data-action=\"remove_undo\""
                                    +   " title=\"" + answer.undo.title + "\""
                                    + ">"
                                    + "<i class=\"fa fa-undo\"></i>"
                                    + "</a>"
                                    )
                                  : ""
                              )
                            + "<b>"
                            + answer.feedback
                            + "</b>"
                            + "</p>"
                            );
                        c$  .addClass ("removed")
                            .data     ("remove_cache", remove_cache)
                            .append   (feedback);
                        if (undo_p) {
                            c$.data   ("remove_undo",  answer.undo);
                        };
                    } else {
                        c$.remove ();
                    };
                    toggle_add_rev_ref (p$);
                };
                var data, success_cb;
                if (elem_pid !== "") {
                    data       =
                        { elem_pid : elem_pid
                        , form_pid : cargo.pid
                        , sid      : cargo.sid
                        , sigs     : sigs
                        , trigger  : F_id
                        }
                    success_cb = function success_cb (answer, status, xhr) {
                        if (! answer ["error"]) {
                            cleanup (answer);
                        } else {
                            $GTW.show_message
                                ("Ajax completion error: ", answer.error);
                        };
                    };
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          : data
                          , success       : success_cb
                          , url           : url
                          }
                        , "Remove"
                        );
                } else {
                    cleanup ();
                };
                return false;
              }
            , reset : function reset (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                var d$    = $(S.display_id_ref, c$).first ();
                var ft    = d$.data ("field_type");
                if (ft) {
                    ft.reset (d$);
                };
                $(S.input_field, c$).each
                    ( function (n) {
                        var f$ = $(this);
                        var ft = f$.data ("field_type");
                        ft.reset (f$);
                      }
                    );
                $(S.focusables, c$).first ().focus ();
                return false;
              }
            };
        var close_section = function close_section (a$) {
            var S     = options.selectors;
            var c$    = a$.closest (S.closable);
            var d$    = $(S.display_id_ref, c$).first ();
            var t$    = $(S.focusables, c$).last ();
            var d     = d$.attr ("value"); // want initial value here
            var fvs   = [];
            var acc   = function acc (n) {
                var f$   = $(this);
                var v    = f$.val ();
                if (v !== "") {
                    fvs.push (v);
                };
            };
            var fs$, i, nxt;
            if (d == "") {
                fs$ = $(":input[id]:not(.prefilled):not(.display)", c$);
                fs$.each (acc);
                d$.val   (fvs.join (", "));
            };
            fs$ = $(S.focusables);
            i   = fs$.index (t$);
            nxt = fs$.get   (i+1);
            if (! nxt) {
                nxt = $(S.submit).first ();
            };
            setTimeout  (function () { nxt.focus (); }, 0);
            c$.addClass ("closed");
        };
        var completer =
            { completed_cb : function completed_cb
                    (f$, f_completer, response, entity_p, cargo) {
                var a$;
                if (response.completions > 0) {
                    if (response.fields > 0) {
                        completer.put_values (response, response.values, cargo);
                    };
                    if ((response.completions == 1) && entity_p) {
                        if ("anchor" in response) {
                            a$ = $("[id=\"" + response.anchor + "\"]");
                        };
                        if (! a$.length) {
                            a$ = f$;
                        };
                        close_section (a$);
                    };
                };
              }
            , get_completions : function get_completions
                    (f$, request, response_cb) {
                var F_id         = f$.prop ("id");
                var c_id         = f$.data ("completer");
                var form_spec    = options.form_spec;
                var cargo        = form_spec.cargo;
                var f_completer  = form_spec.completers [c_id];
                var field_values = completer.get_values
                    (f_completer.buddies_id);
                var data         =
                    { complete_entity : f_completer ["entity_p"] || false
                    , field_values    : field_values
                    , form_pid        : cargo.pid
                    , sid             : cargo.sid
                    , sigs            : cargo.sigs
                    , trigger         : F_id
                    };
                var success_cb = function success_cb (answer, status, xhr) {
                    if (! answer ["error"]) {
                        if (answer.completions > 0 && answer.fields > 0) {
                            completer.get_completions_cb
                                (f$, request, response_cb, f_completer, answer);
                        } else if ("feedback" in answer) {
                            response_cb
                                ( [ { disabled : true
                                    , index    : null
                                    , label    : answer.feedback
                                    , value    : null
                                    }
                                  ]
                                );
                        } else {
                            response_cb ([]);
                        };
                    } else {
                        $GTW.show_message
                            ("Ajax completion error: ", answer.error);
                    };
                };
                // current value not in cargo.field_values yet
                field_values [F_id] = f$.val ();
                $.gtw_ajax_2json
                    ( { async         : true
                      , data          : data
                      , success       : success_cb
                      , url           : options.url.completer
                      }
                    , "Completion"
                    );
              }
            , get_completions_cb : function get_completions_cb
                    (f$, request, response_cb, f_completer, answer) {
                var fields = options.form_spec.buddies
                    [f_completer.buddies_id];
                var l, n   = answer.completions;
                var rl     = answer.fields -
                    (f_completer ["entity_p"] && ! answer.partial); // skip pid
                var v      = answer.fields - 1;
                var result = [];
                if (n > 0 && answer.fields > 0) {
                    l = Math.min (rl, fields.length);
                    f$.data ("gtw_mf3_completer_response", answer);
                    for ( var i = 0, li = answer.matches.length, match
                        ; i < li
                        ; i++
                        ) {
                        match = answer.matches [i];
                        result.push
                            ( { index : i
                              , label :
                                  $.map (match.slice (0, l), bwrap).join ("")
                              , value : match [v]
                              }
                            );
                    };
                };
                response_cb (result);
              }
            , get_values : function get_values (buddies_id) {
                var f_spec = options.form_spec;
                var fields = f_spec.buddies [buddies_id];
                var values = f_spec.cargo.field_values;
                var result = {};
                var id, f$, ft, fv, val;
                for (var i = 0, li = fields.length; i < li; i++) {
                    id = fields [i];
                    fv = values [id];
                    if (fv != undefined) {
                        f$  = field_map [id];
                        if (f$ != undefined) {
                            ft  = f$.data   ("field_type");
                            val = ft.get_cargo (fv);
                            if (val != undefined) {
                                result [id] = val;
                            };
                        };
                    };
                };
                return result;
              }
            , put_values : function put_values (response, match, cargo) {
                var f$, ft, fv, id, val;
                var values = cargo.field_values;
                for (var i = 0, li = response.field_ids.length; i < li; i++) {
                    id   = response.field_ids [i];
                    f$   = $("[id=\"" + id + "\"]");
                    val  = match [i];
                    if (f$.length) {
                        ft = f$.data ("field_type");
                        if (ft != undefined) {
                            // prefilled and readonly fields don't have
                            // `field_type`; they need no action here, anyway
                            ft.put_input (f$, val);
                        };
                        f$.data ("old_value", val);
                    } else {
                        fv = values [id];
                        if (fv != undefined) {
                            fv.edit = val;
                        };
                    };
                };
              }
            , select_cb : function select_cb (ev, f$, item) {
                var data;
                var F_id         = f$.prop ("id");
                var c_id         = f$.data ("completer");
                var form_spec    = options.form_spec;
                var cargo        = form_spec.cargo;
                var f_completer  = form_spec.completers [c_id];
                var response     = f$.data ("gtw_mf3_completer_response");
                var match        = response.matches [item.index];
                var success_cb = function success_cb (answer, status, xhr) {
                    completer.completed_cb
                        (f$, f_completer, answer, true, cargo);
                };
                if (! item.disabled) {
                    // avoid `field_blur_cb` stomping over the new values
                    //
                    // for some reason, `field_blur_cb` doesn't see the
                    // values `completer.put_values` puts from `response`
                    // into the input fields
                    f$.data ("need_blur", false);
                    completer.put_values (response, match, cargo);
                    if (response.partial) {
                        if (! response.finished) {
                            setTimeout
                                (function () { completer.trigger (f$); }, 1);
                        };
                    } else if (response ["entity_p"]) {
                        data  =
                            { complete_entity : true
                            , field_values    :
                                completer.get_values (f_completer.buddies_id)
                            , form_pid        : cargo.pid
                            , pid             : item.value
                            , sid             : cargo.sid
                            , sigs            : cargo.sigs
                            , trigger         : F_id
                            };
                        $.gtw_ajax_2json
                            ( { async         : true
                              , data          : data
                              , success       : success_cb
                              , url           : options.url.completed
                              }
                            , "Completion"
                            );
                    };
                };
              }
            , setup : function setup (n) {
                var f$           = $(this);
                var F_id         = f$.prop ("id");
                var c_id         = f$.data ("completer");
                var form_spec    = options.form_spec;
                var f_completer  = form_spec.completers [c_id];
                if ("choices" in f_completer) {
                    f$.gtw_autocomplete
                        ( { minLength : f_completer.treshold
                          , position  : { collision  : "fit" }
                          , source    : f_completer.choices
                          }
                        );
                } else {
                    f$.gtw_autocomplete
                        ( { focus    : function (ev, ui) {
                                return false;
                            }
                          , minLength : f_completer.treshold
                          , select    : function (ev, ui) {
                                completer.select_cb (ev, f$, ui.item);
                                return false;
                            }
                          , source    : function (request, response_cb) {
                                completer.get_completions
                                    (f$, request, response_cb);
                            }
                          }
                        , "html"
                        );
                };
                if (f_completer.treshold === 0) {
                    f$.focus (completer.trigger_auto_cb);
                };
              }
            , trigger : function trigger (f$) {
                f$.focus ();
                return f$.autocomplete ("search");
              }
            , trigger_auto_cb : function trigger_auto_cb (ev) {
                var f$ = $(this);
                if (f$.val () === "") {
                    f$.autocomplete ("search");
                };
              }
            };
        var field_blur_cb = function field_blur_cb (ev) {
            var S         = options.selectors;
            var f$        = $(this);
            var c$        = f$.closest  (S.composite_field);
            var ft        = f$.data     ("field_type");
            var need_blur = f$.data     ("need_blur");
            var old_value = f$.data     ("old_value");
            var polisher  = f$.data     ("polisher");
            var new_value;
            f$.removeData ("need_blur");
            // only proceed if `need_blur` is set
            // * after completion, `polisher` isn't necessary and shouldn't run
            //   - for some reason, `field_blur_cb` sees the old input values,
            //     not the ones filled in by completion
            // * `completer.select_cb` sets `need_blur` to `false`
            if (need_blur) {
                new_value = ft.get_input (f$);
                if (  polisher
                   && new_value !== ""
                   && ((! old_value) || old_value != new_value)
                   ) {
                    setTimeout
                        ( function () {
                            polish_field (f$, f$.prop ("id"), new_value)
                          }
                        , 0
                        );
                };
            };
        };
        var field_change_cb = function field_change_cb (ev) {
            var S         = options.selectors;
            var form_spec = options.form_spec;
            var f$        = $(this);
            var ft        = f$.data ("field_type");
            var E_id      = closest_el_id (f$, S.form_element);
            var F_id      = f$.prop ("id");
            var req       = f$.prop ("required");
            var l$        = $("label[for='" + F_id + "']");
            var b$        = $(S.status, l$);
            var mf3_value = form_spec.cargo.field_values [F_id];
            var checker   = form_spec.checkers [F_id];
            var status    = true;
            var ini_value, new_value, new_value_p;
            if (mf3_value !== undefined) {
                ini_value      = mf3_value.init;
                new_value      = ft.get_input (f$);
                mf3_value.edit = new_value;
                if (checker) {
                    status = checker (E_id, F_id, form_spec, mf3_value);
                };
                b$.toggleClass ("bad",  !  status)
                  .toggleClass ("good", !! status);
                f$.toggleClass ("bad",  !  status);
                if (req) {
                    new_value_p = ft.truth (new_value);
                    b$.toggleClass ("missing", !  (new_value_p))
                      .toggleClass ("good",    !! (new_value_p && status));
                    f$.toggleClass ("missing", !  (new_value_p));
                };
            };
        };
        var field_focus_cb = function field_focus_cb (ev) {
            var S         = options.selectors;
            var values    = options.form_spec.cargo.field_values;
            var f$        = $(this);
            var c$        = f$.closest (S.composite_field);
            var F_id      = f$.prop ("id");
            var ft        = f$.data ("field_type");
            var fv        = values [F_id];
            f$.data ("old_value", ft.get_cargo (fv))
              .data ("need_blur", true);
        };
        var field_type =
            { checkbox   :
                { clear : function clear_checkbox (f$) {
                    field_type.checkbox.put_input (f$, "");
                  }
                , get_cargo : function get_cargo_checkbox (fv) {
                    return field_type.normal.get_cargo (fv);
                  }
                , get_input : function get_input_checkbox (f$) {
                    var req    = f$.prop ("required");
                    var result = f$.prop ("checked")
                        ? "yes" : (req ? null : "no");
                    return result;
                  }
                , put_cargo : function put_cargo_checkbox (id, value) {
                    field_type.normal.put_cargo (id, value);
                  }
                , put_input : function put_input_checkbox (f$, value) {
                    f$.val ((value == "yes") ? true : false).trigger ("change");
                  }
                , reset : function reset_checkbox (f$, ft) {
                    field_type.normal.reset (f$, ft || field_type.checkbox);
                  }
                , truth : function truth_checkbox (value) {
                    return field_type.normal.truth (value);
                  }
                }
            , id_ref :
                { clear : function clear_id_ref (f$) {
                    field_type.id_ref.put_input (f$, {});
                  }
                , get_cargo : function get_cargo_id_ref (fv) {
                    var edit   = fv ["edit"];
                    var init   = fv ["init"];
                    var result = edit || init;
                    if (result) {
                        result = result.pid;
                    };
                    return result;
                  }
                , get_input : function get_input_id_ref (f$) {
                    var h$ = f$.siblings (".value.hidden.id_ref");
                    var result =
                        { display : f$.val ()
                        , pid     : h$.val ()
                        };
                    return result;
                  }
                , put_cargo : function put_cargo_id_ref (id, value) {
                    if (typeof value === "object") {
                        field_type.normal.put_cargo (id, value);
                    };
                  }
                , put_input : function put_input_id_ref (f$, value) {
                    var h$  = f$.siblings (".value.hidden.id_ref");
                    var id  = f$.prop ("id");
                    var val = $.extend ({display : "", pid : undefined}, value);
                    var fv;
                    if (typeof value === "object") {
                        h$.val (val.pid);
                        f$.val (val.display);
                        field_type.normal.put_cargo (id, val);
                    } else {
                        h$.val (value);
                    };
                  }
                , reset : function reset_id_ref (f$, ft) {
                    field_type.normal.reset (f$, ft || field_type.id_ref);
                  }
                , truth : function truth_id_ref (value) {
                    if (typeof value === "object") {
                        return !! (value ["pid"])
                    } else {
                        return !! value;
                    };
                  }
                }
            , id_ref_select :
                { clear : function clear_id_ref_select (f$) {
                    field_type.id_ref_select.put_input (f$, {});
                  }
                , get_cargo : function get_cargo_id_ref_select (fv) {
                    field_type.id_ref.get_cargo (fv);
                  }
                , get_input : function get_input_id_ref_select (f$) {
                    var elem   = f$.get (0);
                    var value  = f$.val ();
                    var result =
                        { display : elem.item (elem.selectedIndex).label
                        , pid     : f$.val () || -1
                        };
                    return result;
                  }
                , put_cargo : function put_cargo_id_ref_select (id, value) {
                    field_type.id_ref.put_cargo (id, value);
                  }
                , put_input : function put_input_id_ref_select (f$, value) {
                    var id = f$.prop ("id");
                    var val = $.extend ({display : "", pid : undefined}, value);
                    var fv;
                    if (typeof value === "object") {
                        h$.val (val.pid);
                        f$.val (val.display);
                        field_type.normal.put_cargo (id, value);
                    };
                  }
                , reset : function reset_id_ref_select (f$, ft) {
                    field_type.normal.reset
                        (f$, ft || field_type.id_ref_select);
                  }
                , truth : function truth_id_ref_select (value) {
                    return field_type.id_ref.truth (value);
                  }
                }
            , normal :
                { clear : function clear_normal (f$) {
                    field_type.normal.put_input (f$, "");
                  }
                , get_cargo : function get_cargo_normal (fv) {
                    var edit   = fv ["edit"];
                    var init   = fv ["init"];
                    var result = (edit !== undefined) ? edit : init;
                    if (edit === "" && edit === init) {
                        result = undefined;
                    };
                    return result;
                  }
                , get_input : function get_input_normal (f$) {
                    return f$.val ();
                  }
                , put_cargo : function put_cargo_normal (id, value) {
                    var fv = options.form_spec.cargo.field_values [id];
                    if (fv != undefined) {
                        fv.edit = value;
                    };
                  }
                , put_input : function put_input_normal (f$, value) {
                    f$.val (value).trigger ("change");
                  }
                , reset : function reset_normal (f$, ft) {
                    var id = f$.prop ("id");
                    var fv = options.form_spec.cargo.field_values [id];
                    (ft || field_type.normal).put_input (f$, fv.init);
                  }
                , truth : function truth_normal (value) {
                    return !! value;
                  }
                }
            , _setup : function _setup (n) {
                var f$ = $(this);
                var id = f$.prop ("id");
                var typ;
                if (f$.attr ("type") == "checkbox") {
                    typ = field_type.checkbox;
                } else if (f$.is (".id_ref_select")) {
                    typ = field_type.id_ref_select;
                } else if (f$.is (".id_ref")) {
                    typ = field_type.id_ref;
                } else {
                    typ = field_type.normal;
                };
                f$.data ("field_type", typ);
                field_map [id] = f$;
              }
            };
        var form_errors =
            { container : function container () {
                var S      = options.selectors;
                var form$  = options.form$;
                var result = $(S.form_errors, form$);
                if (! result.length) {
                    $("h1", form$).first ().after ($( L (S.form_errors)));
                    result = $(S.form_errors, form$);
                };
                return result;
              }
            , display : function display (errors) {
                var errs$ = form_errors.container ();
                var form$ = options.form$;
                $("aside .error-msg", form$).remove ();
                errs$.html
                    ($(L ("h1", { html : translated ("Form errors")})));
                for (var i = 0, li = errors.length, err; i < li; i++) {
                    err = errors [i];
                    form_errors.display_1 (errs$, err);
                };
                $(err_ref, errs$).addClass ("pure-button");
                errs$.show ();
                $(err_ref, errs$).first ().trigger ("click");
                //$GTW.show_message ("Submit errors: ", errors);
              }
            , display_1 : function display_1 (errs$, err) {
                var S      = options.selectors;
                var ent$   = $("[id=\"" + err.entity + "\"]");
                var err$   = $(L (S.err_msg));
                var a$, f$, r$, desc;
                if (ent$.length) {
                    ent$.closest (S.closable).removeClass ("closed");
                };
                errs$.append (err$);
                err$.append  ($( L ( "h2", { html : err.head })));
                if ("description" in err) {
                    desc = err.description;
                    err$.append ($(L ("p.description", { html : desc })));
                };
                if ("explanation" in err) {
                    err$.append
                        ($(L ("p.explanation", { html : err.explanation })));
                };
                for (var i = 0, li = err.fields.length, f; i < li; i++) {
                    f  = err.fields [i];
                    f$ = $("[id=\"" + f.fid + "\"]");
                    r$ = $(err_ref + "[data-id=\"" + f.fid + "\"]");
                    f$.toggleClass ("bad",  true)
                      .toggleClass ("good", false);
                    r$.prop
                        ( "title"
                        , translated ("Correct field") + " " + f.label
                        );
                    if (desc) {
                        a$ = f$.siblings ().filter ($("aside"));
                        a$.append ($(L ("p.error-msg", { html : desc })));
                    };
                }
              }
            , goto_field : function goto_field (ev) {
                var S       = options.selectors;
                var a$      = $(this);
                var id      = a$.data ("id");
                var f$      = $("[id=\"" + id + "\"]");
                f$.focus ();
                return false;
              }
            };
        var polish_field = function polish_field (f$, F_id, new_value) {
            var buddies_id   = f$.data ("polisher");
            var form_spec    = options.form_spec;
            var cargo        = form_spec.cargo;
            var field_values = completer.get_values (buddies_id);
            var success_cb   = function success_cb (answer, status, xhr) {
                var a$;
                if (! answer ["error"]) {
                    a$ = f$.siblings ().filter ($("aside"));
                    $("p.error-msg.polish", a$).remove ();
                    if ("field_values" in answer) {
                        completer.put_values
                            (answer, answer.field_values, cargo);
                    };
                    if ("feedback" in answer) {
                        a$.append
                            ($(L ("p.error-msg.polish"
                                 , { html : answer.feedback }
                                 )
                              )
                            );
                        setTimeout (function () { f$.focus (); }, 0);
                    };
                } else {
                    $GTW.show_message
                        ("Ajax polisher error: ", answer.error);
                };
            };
            var data;
            field_values [F_id] = new_value;
            data =
                { field_values    : field_values
                , form_pid        : cargo.pid
                , sid             : cargo.sid
                , sigs            : cargo.sigs
                , trigger         : F_id
                };
            $.gtw_ajax_2json
                ( { async         : true
                  , data          : data
                  , success       : success_cb
                  , url           : options.url.polisher
                  }
                , "Polish"
                );
        };
        var remove_undo_cb = function remove_undo_cb (ev) {
            var S            = options.selectors;
            var a$           = $(ev.currentTarget);
            var c$           = a$.closest (S.closable);
            var p$           = c$.closest (S.entity_list);
            var remove_cache = c$.data    ("remove_cache");
            var undo         = c$.data    ("remove_undo");
            var form_spec    = options.form_spec;
            var cargo        = form_spec.cargo;
            var f_values     = cargo.field_values;
            var sigs         = cargo.sigs;
            var success_cb   = function success_cb (response, status) {
                if (! response ["error"]) {
                    $.extend         (cargo.field_values, remove_cache.vals);
                    $.extend         (cargo.sigs,         remove_cache.sigs);
                    c$  .data        ("remove_cache",     undefined)
                        .data        ("remove_undo",      undefined)
                        .removeClass ("removed");
                    $("p.feedback", c$).remove ();
                    toggle_add_rev_ref (p$);
                } else {
                    $GTW.show_message ("Ajax Error: " + response ["error"]);
                };
            };
            $.gtw_ajax_2json
                ( { type        : "POST"
                  , data        : undo
                  , success     : success_cb
                  , url         : undo.url
                  }
                , "Undo"
                );
            return false;
        };
        var setup_entity_display = function setup_entity_display (n) {
            var S  = options.selectors;
            var f$ = $(this);
            var s$ = f$.closest (S.container);
            var d$ = $(S.display_id_ref, f$).first ();
            var ak = d$.data ("action") || "open"
            s$.gtw_hd_input
                ( { callback       : action_callback [ak]
                  , clear_callback : action_callback.clear
                  , key_ignore_hi  : 27               // escape
                  , trigger_event  : "click keydown"
                  }
                );
        };
        var setup_esf_selector = function setup_esf_selector (n) {
            var S         = options.selectors;
            var cargo     = options.form_spec.cargo;
            var f$        = $(this);
            var E_id      = closest_el_id (f$, S.form_element);
            var F_id      = f$.prop ("id");
            var s$        = f$.closest (S.container);
            var selector  = s$.data ("gtw_e_type_selector_mf3");
            var apply_cb  = function apply_cb (display, value) {
                field_type.id_ref.put_input
                    (f$, { display : display, pid : value});
            };
            if (! selector) {
                s$.gtw_e_type_selector_hd_mf3
                    ( { mf3 :
                          { apply_cb  : apply_cb
                          , E_id      : E_id
                          , F_id      : F_id
                          , pid       : cargo.pid
                          , sid       : cargo.sid
                          , sigs      : cargo.sigs
                          }
                      , url : options.url
                      }
                    );
            };
        };
        var setup_fields = function setup_fields (context) {
            var S     = options.selectors;
            var dfs$  = $(S.display_field,   context);
            var idfs$ = $(S.input_field,     context);
            var infs$ = $(S.input_field,     context);
            var ffs$  = $(S.focusables,      context);
            dfs$.each      (setup_entity_display);
            idfs$.each     (field_type._setup)
                .change    (field_change_cb)
                .trigger   ("change");
            infs$
                .blur      (field_blur_cb)
                .focus     (field_focus_cb)
                .filter    ("[data-completer]")
                    .each  (completer.setup)
                    .end   ()
                .filter    (".Selector .display")
                    .each  (setup_esf_selector)
                    .end   ();
            ffs$.addClass  ("focusable")
                .first     (":input")
                    .focus ()
                    .end   ();
        };
        var setup_sub_form = function setup_sub_form (f$) {
            var action;
            setup_fields (f$);
            for (action in action_callback) {
                if (action_callback.hasOwnProperty (action)) {
                    $("[data-action=\"" + action + "\"]", f$)
                        .on ("click", action_callback [action]);
                };
            };
        };
        var show_field_desc_cb = function show_field_desc_cb (ev) {
            var S            = options.selectors;
            var target$      = $(ev.target);
            var show_p       = window.getComputedStyle
                (document.body, ":after").getPropertyValue ("font-size");
            var x$;
            if (show_p != "0px") {
                x$ = target$.siblings ().filter (S.field_desc);
                x$.toggleClass ("open");
            };
            return true;
        };
        var submit_cb = function submit_cb (ev) {
            var S            = options.selectors;
            var form$        = options.form$;
            var target$      = $(ev.target);
            var form_spec    = options.form_spec;
            var name         = target$.prop ("name");
            var url          = form$.prop ("action") || document.URL;
            var f_act        = $(":input[name=F_ACT]", form$).val ();
            var json_data    =
                { cancel : (name == "cancel")
                , cargo  : form_spec.cargo
                , F_ACT  : f_act
                , next   : options.url.next
                };
            var pre_submit_callbacks = options.pre_submit_callbacks;
            var success_cb = function success_cb (answer, status, xhr) {
                if (! answer ["error"]) {
                    $(S.form_errors, form$).hide ();
                    if (answer ["conflicts"]) {
                        // XXX
                        $GTW.show_message
                            ("Submit conflicts", answer.conflicts);
                    } else if (answer ["errors"]) {
                        form_errors.display (answer.errors);
                    } else if (answer ["expired"]) {
                        // XXX display re-authorization form
                        $GTW.show_message ("Expired: ", answer.expired);
                    } else if (answer ["feedback"]) {
                        $(":input, button, .action-button a", form$)
                            .addClass ("ui-state-disabled") // ???
                            .prop     ("disabled", true);
                        form$.before (answer.feedback);
                    } else {
                        // Need timeout here for IE
                        setTimeout
                            ( function () {
                                window.location.href = options.url.next;
                              }
                            , 0
                            );
                    };
                } else {
                    $GTW.show_message ("Submit error: ", answer ["error"]);
                };
            };
            json_data [name] = true;
            if (ev && "preventDefault" in ev) {
                ev.preventDefault ();
            };
            for (var i = 0, li = pre_submit_callbacks.length; i < li; i++) {
                pre_submit_callbacks [i] ();
            };
            $.gtw_ajax_2json
                ( { url         : url
                  , data        : json_data
                  , success     : success_cb
                  }
                , "Submit"
                );
            return false;
        };
        var toggle_add_rev_ref = function toggle_add_rev_ref (c$) {
            var S      = options.selectors;
            var max_rr = c$.data     ("max-rev-ref");
            var rr$    = c$.children (S.container_rev_ref).not (".removed");
            var ab$    = $("[data-ref=\"" + c$.prop ("id") + "\"]", c$);
            ab$.toggle (rr$.length < max_rr);
        };
        var translated = function translated (text) {
            var result = text;
            if (text in options.texts) {
                result = options.texts [text];
            };
            return result;
        }
        var err_ref   = selectors.err_msg + " a";
        options.form$ = this;
        this.delegate  (err_ref, "click", form_errors.goto_field);
        this.delegate
            (selectors.label_with_desc, "click", show_field_desc_cb);
        // bind `submit_cb` to `click` of submit buttons (need button name)
        // disable `submit` event for form to avoid IE to do normal form
        // submit after running `submit_cb`
        this.delegate  (selectors.submit, "click", submit_cb);
        this.submit    (function (ev) { return false; });
        setup_sub_form (this);
        $(this).on ("click", "[data-action=\"remove_undo\"]", remove_undo_cb);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/mf3.js
