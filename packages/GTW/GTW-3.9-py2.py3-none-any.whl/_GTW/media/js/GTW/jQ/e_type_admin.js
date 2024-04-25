// Copyright (C) 2011-2015 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/e_type_admin.js
//
// Purpose
//    jQuery plugin for GTW.NAV.E_Type.Admin pages
//
// Revision Dates
//    26-Nov-2011 (CT) Creation
//    21-Feb-2012 (CT) Use `$GTW.L` to create DOM elements
//    19-Apr-2012 (CT) Add `options.postify_options.hidden_selector`
//    11-Mar-2014 (CT) Add hasClass `link` to `gtw_e_type_admin_linkify `
//    22-Jan-2015 (CT) Adapt to change of `.Object-List` table
//    28-May-2015 (CT) Revamp action handling, remove use of `gtw_postify_a`
//    29-May-2015 (CT) Add `action_callback.undo`,
//                     add `undo` to `action_callback.remove`
//    29-May-2015 (CT) Factor `setup_action_callbacks`, `setup_obj_row`
//    ««revision-date»»···
//--

( function ($) {
    "use strict";
    $.fn.gtw_e_type_admin_table = function gtw_e_type_admin_table (opts) {
        var action;
        var selectors       = $.extend
            ( { obj_col            : "td:not(.action):not(.link)"
              , obj_row            : "tr[id]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options         = $.extend
            ( { tr_class    : "active"
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        var pat_pid         = new RegExp ("^([^-]+)-(\\d+)$");
        var action_callback =
            { change : function change (ev) {
                var obj = obj_of_row (this);
                var url = obj.url;
                setTimeout
                    ( function () {
                        window.location.href = url;
                      }
                    , 0
                    );
                return false;
              }
            , remove : function remove (ev) {
                var obj = obj_of_row (this);
                var success_cb  = function success_cb (response, status) {
                    var row$ = obj.row$;
                    var cs   = $("td",        row$).length;
                    var csa  = $("td.action", row$).length;
                    var repl, undo_p;
                    if (! response ["error"]) {
                        undo_p = "undo" in response;
                        repl   =
                            ( "<td class=\"feedback\" colspan=\""
                            + (undo_p ? cs - csa : cs)
                            + "\">"
                            + response.feedback
                            + "</td>"
                            );
                        if (undo_p) {
                            row$.data ("deleted", row$.html ());
                            row$.data ("undo",    response.undo);
                            repl =
                                ( repl
                                + "<td class=\"action\">"
                                + "<a class=\"pure-button\" data-action=\"undo\""
                                + "title=\"" + response.undo.title + "\""
                                + ">"
                                + "<i class=\"fa fa-undo\"></i>"
                                + "</a>"
                                + "</td>"
                                );
                        };
                        row$.html (repl);
                        row$.prop ("title", "");
                        setup_action_callbacks (row$);
                    } else {
                        $GTW.show_message ("Ajax Error: " + response ["error"]);
                    };
                };
                $.gtw_ajax_2json
                    ( { type        : "DELETE"
                      , success     : success_cb
                      , url         : obj.url
                      }
                    , "Delete"
                    );
                return false;
              }
            , undo : function undo (ev) {
                var obj  = obj_of_row (this);
                var row$ = obj.row$;
                var rest = row$.data ("deleted");
                var undo = row$.data ("undo");
                var success_cb = function success_cb (response, status) {
                    if (! response ["error"]) {
                        row$.html     (rest);
                        row$.data     ("deleted", undefined);
                        row$.data     ("undo",    undefined);
                        setup_obj_row (row$);
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
              }
            };
        var obj_of_row  = function obj_of_row (self) {
            var result  = {};
            var row$    = $(self).closest  (selectors.obj_row)
            result.row$ = row$;
            result.rid  = row$.prop        ("id");
            result.pid  = pid_of_obj_id    (result.rid);
            result.url  = row$.data        ("href");
            return result;
        };
        var pid_of_obj_id = function pid_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [2];
        };
        var setup_action_callbacks = function setup_action_callbacks (self) {
            for (action in action_callback) {
                if (action_callback.hasOwnProperty (action)) {
                    $("[data-action=\"" + action + "\"]", self)
                        .on ("click", action_callback [action]);
                };
            };
        };
        var setup_obj_row = function setup_obj_row (self) {
            var ac$  = self.find ("[data-action=\"change\"]");
            setup_action_callbacks (self);
            if (ac$.length) {
                self.addClass (options.tr_class)
                   .attr ("title", ac$.attr ("title"));
                $(selectors.obj_col, self).click (action_callback.change);
            };
        };
        $(selectors.obj_row, this).each
            (function () { setup_obj_row ($(this)); });
        return this;
    };
    ( function () {
        var setup_obj_list = function setup_obj_list () {
            var options = $GTW.ETA$.options;
            $(options.obj_list_selector).gtw_e_type_admin_table ();
        };
        $GTW.ETA$ = new $GTW.Module (
            { options            :
                { obj_list_selector   : ".Object-List"
                }
            , setup_obj_list     : setup_obj_list
            }
        );
      } ()
    );
  } (jQuery)
);

// __END__ GTW/jQ/e_type_admin.js
