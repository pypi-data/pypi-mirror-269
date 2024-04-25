// Copyright (C) 2011-2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/e_type_selector.js
//
// Purpose
//    jQuery plugin for selecting an specific instance of a MOM E_Type using
//    autocompletion
//
// Revision Dates
//    15-Dec-2011 (CT) Creation
//    16-Dec-2011 (CT) Cache `ajax_response`
//    21-Dec-2011 (CT) Set `title` in `apply_cb`
//    21-Dec-2011 (CT) Change `select_cb` to not repeat partial search after
//                     a single match
//    24-Feb-2012 (CT) Change `get_completions` to handle `n == 0` correctly
//     7-Mar-2012 (CT) Factor `ET_Selector` and `ET_Selector_HD`
//     7-Mar-2012 (CT) Add `ET_Selector_AFS`, refactor as necessary
//     8-Mar-2012 (CT) Fix bugs in `ET_Selector_AFS`, `ET_Selector_HD`
//     8-Mar-2012 (CT) Add `options.completer_position` and `.dialog_position`
//     3-Apr-2013 (CT) Split hidden `input` field "__attribute_selector_for__"
//                     into two: "__esf_for_attr__"  and "__esf_for_type__"
//     4-Apr-2013 (CT) Factor `setup_form` from `setup_widget`
//     4-Apr-2013 (CT) Add support for `esf_polymorphic`
//     5-Apr-2013 (CT) Adapt to API changes of jQueryUI 1.9+
//     5-Apr-2013 (CT) Add gtw-specific prefix to .`data` keys
//     9-Apr-2013 (CT) Fix `close` callback of `.dialog`
//    10-Apr-2013 (CT) Bind `beforeClose`, `close` events of `dialog` to
//                     `before_close_cb`, `close_cb`;
//                     bind `cancel_button` to `close` calling `dialog("close")`
//    22-Apr-2013 (CT) Change default of `treshold` to `0`
//    29-Apr-2013 (CT) Use `$GTW.show_message`, not `console.error`
//     1-May-2013 (CT) Change `gtw_e_type_selector_afs` to
//                     `gtw_e_type_selector_hd_afs`
//    20-Jan-2014 (CT) Change `apply_cb` and`clear_cb` to pass cleared
//                     `response` to `_apply_cb_inner`
//    28-Apr-2014 (CT) Add `ET_Selector_MF3`, `gtw_e_type_selector_hd_mf3`
//    30-Apr-2014 (CT) Fix `ET_Selector_MF3`
//     3-May-2014 (CT) Use `trigger_event : "click keydown"` for `_MF3`
//    15-May-2014 (CT) Change `gtw_e_type_selector_hd_mf3` to ignore all
//                     control characters between `tab` and `escape`
//                     (which includes the shift key)
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    24-Aug-2014 (CT) Add `form_pid`, `sid`, `sigs` to `result` of
//                     `ET_Selector_MF3.get_esf_data` and `.get_completion_data`
//    24-Aug-2014 (CT) Remove `key` from `result`of
//                     `ET_Selector_MF3.get_completion_data`
//    24-Aug-2014 (CT) Change `get_completions` to always fill `values`
//                     (i.e., remove guard for `self.completion_data.key`)
//    28-Aug-2014 (CT) Finetune keys ignored by `gtw_e_type_selector_hd_mf3`
//                     (e.g., add `cursor left`, `end`, and some others)
//    15-Sep-2014 (CT) Change `default_position` from `right` to `left`
//     5-Dec-2014 (CT) Use pure, not jqueryui, buttons
//    15-Jan-2015 (CT) Factor key handling to `gtw_hd_input`
//    15-Jan-2015 (CT) Change `gtw_e_type_selector_hd` to use "click keydown"
//                     as `trigger_event`
//    16-Jan-2015 (CT) Fix `setup_form`
//                     * exclude inputs with `type=hidden`
//                     * do setup only once
//    16-Jan-2015 (CT) Change `setup_widget` to use `ui.panel` of `create` event
//                     * `ui.content` was deprecated in jqueryui 1.10,
//                       and was removed in jqueryui 1.11
//                     * missed that during the upgrade to 1.10
//    26-Mar-2015 (CT) Change `activate_cb` to display possible completions
//                     automatically, if `treshold === 0`
//    27-Mar-2015 (CT) Use `flipfit`, not `fit`, for `collision`
//    31-Mar-2015 (CT) Use `fit`, not `flipfit`, for `collision`
//                     (`flipfit` truncates on the left of completion info)
//    31-Mar-2015 (CT) Set CSS `overflow` to `visible` for `dialog`
//     1-Apr-2015 (CT) Add dialog class `no-close`
//     1-Apr-2015 (CT) Handle multiple calls of `activate_cb` gracefully
//                     + `focus` 1.input in `activate_cb`, not `setup_form`
//                     + change `close_cb` to reset `.widget`
//     1-Apr-2015 (CT) Focus `apply_button` in `completed_cb`
//     1-Apr-2015 (CT) Add `max-height`, `max-width`, `min-width` to
//                     `autocomplete.css`
//     1-Apr-2015 (CT) Mark non-matching input with class `bad`
//     2-Apr-2015 (CT) Add `feedback` to `get_ccb`
//    12-May-2015 (CT) Rename `inputs$` to `user_inputs$`
//    12-May-2015 (CT) Change `clear_cb` to use `user_inputs$`,
//                     not home-grown code; put focus on `input1$`
//    15-Dec-2015 (CT) Remove obsolete AFS related functions
//    25-May-2016 (CT) Add `select_e_type_cb`, `af_polymorphic`
//    25-May-2016 (CT) Factor `selector.user_inputs`, `field_values`
//     6-Jun-2016 (CT) Add `trigger`, `trigger_n` to `select_cb`
//     7-Jun-2016 (CT) Remove `esf_polymorphic`
//    10-Jun-2016 (CT) Change `completed_cb` to use `response.values`,
//                     not `response.html`, i.e., update, not replace, ESF form
//    ««revision-date»»···
//--

( function ($, undefined) {
    "use strict";

    var bwrap = function bwrap (v) {
        return "<b>" + v + "</b>";
    };
    var default_position =
        { my         : "left top"
        , at         : "left bottom"
        , collision  : "fit"
        };
    var ET_Selector = $GTW.Class.extend (
        { defaults              :
            { closing_flag        : "gtw_esf_closing"
            , completer_position  : default_position
            , dialog_position     : default_position
            , icon_map            : {}
            , selectors           :
                { aid             : "[name=__esf_for_attr__]"
                , af_polymorphic  : ".attr-filter.polymorphic"
                , fieldset_e_type : "fieldset.E_Type"
                , select_e_type   : "select.E_Type"
                , tid             : "[name=__esf_for_type__]"
                , user_inputs     :
                    ":input:not([type=hidden]):not(button):not(.hidden)"
                }
            , treshold            : 0
            }
        , init                  : function init (opts) {
              var icon_map = $.extend
                  ( {}
                  , this.defaults.icon_map
                  , opts && opts ["icon_map"] || {}
                  );
              var completer_position, dialog_position;
              var S;
              this.icons     = new $GTW.FA_Icon_Map (icon_map);
              S = $.extend
                  ( {}
                  , this.defaults.selectors
                  , this.icons.selectors
                  , opts && opts ["selectors"] || {}
                  );
              completer_position = $.extend
                  ( {}
                  , this.defaults.completer_position
                  , opts && opts ["completer_position"] || {}
                  );
              dialog_position = $.extend
                  ( {}
                  , this.defaults.dialog_position
                  , opts && opts ["dialog_position"] || {}
                  );
              this.options = $.extend
                  ( {}
                  , this.defaults
                  , opts || {}
                  , { icon_map           : this.icons
                    , completer_position : completer_position
                    , dialog_position    : dialog_position
                    }
                  );
              this.selectors = $.extend
                  ( {}
                  , S
                  , { user_inputs     :
                        S.user_inputs + ":not(" + S.select_e_type + ")"
                    }
                  );
              this.options.selectors = this.selectors;
              this.ajax_response = undefined;
              this.hd_input$     = undefined;
              this.widget        = undefined;
          }
        , activate_cb           : function activate_cb (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              var input1$, val1;
              self.target$  = $(ev.delegateTarget);
              self.esf_data = self.get_esf_data (ev, self.target$);
              if (! self.ajax_response) {
                  $.gtw_ajax_2json
                      ( { async       : false
                        , data        : self.esf_data
                        , success     : function (response, status) {
                              if (! response ["error"]) {
                                  if ("html" in response) {
                                      self.ajax_response = response;
                                      self.widget        = self.setup_widget
                                          (response);
                                  } else {
                                    $GTW.show_message ("Ajax Error", response);
                                  }
                              } else {
                                  $GTW.show_message ("Ajax Error", response.error);
                              };
                          }
                        , url         : self.options.url.qx_esf
                        }
                      , "Entity completer"
                      );
              } else if (! self.widget) {
                  self.widget = self.setup_widget (self.ajax_response);
              };
              input1$ = self.user_inputs$.filter (":visible").eq (0);
              input1$.focus ();
              if (self.options.treshold === 0) {
                  val1 = input1$.val ();
                  if (val1 === "") {
                      // display possible completions, automatically
                      input1$.autocomplete ("search");
                  };
              };
              return false;
          }
        , activate_form         : function activate_form (form) {
              if (form) {
                  this.setup_form ($(form));
              };
          }
        , apply_cb              : function apply_cb (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              var response = self.widget.data ("gtw_ets_completed_response");
              if (! response) {
                  // no repsonse from `completed_cb`
                  //     --> clear `display`, `value`
                  response = { display : "", value : null };
              };
              self._apply_cb_inner (ev, response);
              self.close ();
              if ("esf_focusee" in self.options) {
                  self.options.esf_focusee.focus ();
              };
              return false;
          }
        , before_close_cb       : function before_close_cb (ev, ui) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              var hdi$ = self.hd_input$;
              if (hdi$) {
                  hdi$.data (self.options.closing_flag, true);
              };
          }
        , clear_cb              : function clear_cb (ev) {
              var self    = (ev && "data" in ev) ? ev.data || this : this;
              var S       = self.options.selectors;
              var ab$     = self.a_form$.find (S.apply_button);
              var input1$ = self.user_inputs$.filter (":visible").eq (0);
              // clear all input fields
              self.user_inputs$.val ("");
              // enable `apply` but reset `gtw_ets_completed_response`, if any
              // if the user clicks to `apply` button, the associated input
              // will be cleared
              ab$.gtw_button_pure ("option", "disabled", false);
              self.widget.data    ("gtw_ets_completed_response", null);
              input1$.focus       ();
          }
        , close                 : function close (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              self.widget.dialog ("close");
          }
        , close_cb              : function close_cb (ev, ui) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              var hdi$ = self.hd_input$;
              try {
                  self.widget.dialog ("destroy");
                  self.widget = null;
              } finally {
                  if (hdi$) {
                      hdi$.removeData (self.options.closing_flag);
                  };
              };
          }
        , completed_cb          : function completed_cb (inp$, response) {
              var S = this.options.selectors;
              this.user_inputs$
                  .each
                      ( function () {
                          var k = this.id;
                          var v = response.values [k];
                          if (k && v !== undefined) {
                              $V5a.form_field.put (this, v);
                          };
                        }
                      );
              this.widget
                  .data ("gtw_ets_completed_response", response);
              this.a_form$
                  .find (S.apply_button)
                      .gtw_button_pure ("option", "disabled", false)
                      .focus ();
          }
        , field_values          : function field_values () {
              var self   = this;
              var values = {}, n = 0;
              self.a_form$
                  // don't use `self.user_inputs$` because we need
                  // inputs with `[type=hidden]`, too, here
                  .find (":input").not ("button, .hidden, [disabled]")
                  .each
                      ( function () {
                          var i$ = $(this);
                          var k  = i$.prop ("id");
                          var v  = i$.val  ();
                          if (k && v) {
                              values [k] = v;
                              n += 1;
                          };
                        }
                      );
              return { map : values, n : n };
          }
        , get_ccb               : function get_ccb (inp$, term, cb, response) {
              var S = this.options.selectors;
              var l = response.fields - !response.partial; // skip pid
              var v = response.fields - 1;
              var result = [];
              var label;
              inp$.data ("gtw_ets_completer_response", response);
              if (response.completions > 0) {
                  inp$.removeClass ("bad");
                  if (response.fields > 0) {
                      for ( var i = 0, li = response.matches.length, match
                          ; i < li
                          ; i++
                          ) {
                          match = response.matches [i];
                          label = $.map (match.slice (0, l), bwrap).join ("");
                          result.push
                              ( { index : i
                                , label : label
                                , value : match [v]
                                }
                              );
                      };
                  } else if ("feedback" in response) {
                      result.push
                          ( { disabled : true
                            , index    : null
                            , label    : response.feedback
                            , value    : null
                            }
                          );
                  };
              } else {
                  inp$.addClass ("bad");
                  this.a_form$
                      .find (S.apply_button)
                          .gtw_button_pure ("option", "disabled", true);
              };
              cb (result);
          }
        , get_completions       : function get_completions (inp$, term, cb) {
              var self     = this;
              var options  = self.options;
              var S        = options.selectors;
              var trigger  = inp$.prop ("id");
              var values   = self.field_values ();
              self.completion_data = self.get_completion_data ();
              if (values.n > 0 || options.treshold == 0) {
                  $.gtw_ajax_2json
                      ( { async         : true
                        , data          : $.extend
                            ( { entity_p  : true
                              , trigger   : trigger
                              , trigger_n : trigger
                              , values    : values.map
                              }
                            , self.completion_data
                            )
                        , success       : function (answer, status, xhr) {
                            if (! answer ["error"]) {
                                self.get_ccb (inp$, term, cb, answer);
                            } else {
                                $GTW.show_message
                                  ("Ajax error", answer.error, data);
                            };
                          }
                        , url           : options.url.qx_esf_completer
                        }
                      , "Completion"
                      );
              } else {
                  cb ([]);
              };
          }
        , select_cb             : function select_cb (ev, inp$, item) {
              var self     = this;
              var S        = self.options.selectors;
              var response = inp$.data ("gtw_ets_completer_response");
              var trigger  = inp$.prop ("id");
              var values   = self.field_values ();
              if (! item.disabled) {
                  if (response.partial) {
                      inp$.val (item.value);
                      if (response.matches.length > 1) {
                          setTimeout
                              ( function () {
                                  inp$.focus ();
                                  inp$.autocomplete ("search");
                                }
                              , 1
                              );
                      } else {
                          self.user_inputs$
                              .filter (":visible")
                              .eq     (item.index + 1)
                              .focus ();
                      };
                  } else {
                      $.gtw_ajax_2json
                          ( { async         : true
                            , data          : $.extend
                                ( { pid       : item.value
                                  , trigger   : trigger
                                  , trigger_n : trigger
                                  , values    : values.map
                                  }
                                , self.completion_data
                                )
                            , success       : function (answer, status, xhr) {
                                  self.completed_cb (inp$, answer);
                              }
                            , url           : self.options.url.qx_esf_completed
                            }
                          , "Completion"
                          );
                  };
              };
          }
        , select_e_type_cb      : function select_e_type_cb (ev) {
              var self    = (ev && "data" in ev) ? ev.data || this : this;
              var S       = self.options.selectors;
              var f$      = $(ev.delegateTarget);
              var c$      = f$.closest (S.af_polymorphic);
              var fsets$  = $(S.fieldset_e_type, c$);
              var e_type  = f$.val ();
              var fset$;
              fsets$.each
                  ( function () {
                      var disabled  = !
                          (e_type && this.classList.contains (e_type));
                      this.disabled = disabled;
                      if (! disabled) {
                          fset$ = $(this);
                      };
                    }
                  );
              self.clear_cb (ev);
          }
        , setup_form            : function setup_form (form$) {
              var self         = this;
              var options      = self.options;
              var S            = options.selectors;
              var user_inputs$ = form$.find (S.user_inputs);
              var select_et$   = form$.find (S.select_e_type);
              var height       = $(window).height ();
              var width        = $(window).width  ();
              var css_spec     =
                  { "max-height" : height * 0.6
                  , "max-width"  : width  * 0.8
                  , "min-width"  : width  * (width  < 680 ? 0.8 : 0.5)
                  };
              if (this.a_form$ !== form$) {
                  this.a_form$      = form$;
                  this.user_inputs$ = user_inputs$;
                  form$.submit (self, self.apply_cb);
                  user_inputs$.each
                      ( function () {
                          var inp$ = $(this);
                          inp$.gtw_autocomplete
                              ( { focus     : function (event, ui) {
                                      return false;
                                  }
                                , minLength : options.treshold
                                , position  : options.completer_position
                                , select    : function (event, ui) {
                                      self.select_cb (event, inp$, ui.item);
                                      return false;
                                  }
                                , source    : function (req, cb) {
                                      self.get_completions (inp$, req.term, cb);
                                  }
                                }
                              , "html"
                              ).autocomplete ("widget").css (css_spec);
                        }
                      );
                  select_et$.change (self, self.select_e_type_cb);
              };
          }
        , setup_widget          : function setup_widget (response) {
              var self    = this;
              var options = self.options;
              var S       = options.selectors;
              var active  = "selected_type" in response ?
                                response.selected_type : false;
              var result  = $(response.html)
                  .dialog
                      ( { autoOpen    : false
                        , beforeClose : function (ev, ui)
                            { self.before_close_cb (ev, ui); }
                        , close       : function (ev, ui)
                            { self.close_cb (ev, ui); }
                        , dialogClass : "no-close"
                        }
                      );
              var form$;
              result.find  (S.button).gtw_button_pure ({icon_map : this.icons});
              result.find  (S.apply_button)
                  .gtw_button_pure ("option", "disabled", true)
                  .click   (self, self.apply_cb);
              result.find  (S.cancel_button).click (self, self.close);
              result.find  (S.clear_button).click  (self, self.clear_cb);
              result
                  .dialog ("option", "width", "auto")
                  .dialog ("open")
                  .dialog ("widget")
                      // make large autocompletion menus visible outside the
                      // dialog widget
                      .css ("overflow", "visible")
                      .position
                          ( $.extend
                              ( {}
                              , options.dialog_position
                              , { of : self.target$ }
                              )
                          );
              form$ = result.is ("form") ? result : result.find ("form");
              this.setup_form (form$);
              return result;
          }
        }
    );
    var ET_Selector_MF3 = ET_Selector.extend (
        { get_completion_data   : function get_completion_data () {
              var opts   = this.options;
              var mf3    = opts.mf3;
              var tid$   = this.a_form$.find (opts.selectors.tid);
              var result =
                  { fid      : mf3.E_id
                  , form_pid : mf3.pid
                  , sid      : mf3.sid
                  , sigs     : mf3.sigs
                  , trigger  : mf3.F_id
                  };
              return result;
          }
        , get_esf_data          : function get_esf_data (ev, target$) {
              var mf3    = this.options.mf3;
              var result =
                  { fid      : mf3.E_id
                  , form_pid : mf3.pid
                  , sid      : mf3.sid
                  , sigs     : mf3.sigs
                  , trigger  : mf3.F_id
                  };
              return result;
          }
        , _apply_cb_inner       : function (ev, response) {
              var opts    = this.options;
              var hidden$ = this.target$.siblings
                  (opts.selectors ["hidden"] || ".value.hidden").first ();
              this.target$
                  .prop ("title", response.display)
                  .val  (response.display);
              hidden$
                  .val  (response.value);
              this.options.mf3.apply_cb (response.display, response.value);
          }
        }
    );
    var ET_Selector_HD = ET_Selector.extend (
        { get_completion_data   : function get_completion_data () {
              var opts   = this.options;
              var aid$   = this.a_form$.find (opts.selectors.aid);
              var tid$   = this.a_form$.find (opts.selectors.tid);
              var result =
                  { key  : aid$.val ()
                  };
              return result;
          }
        , get_esf_data          : function get_esf_data (ev, target$) {
              return { key : target$.prop ("id") };
          }
        , _apply_cb_inner       : function (ev, response) {
              var hidden$ = this.target$.siblings
                  ("[name=\"" + this.esf_data.key + "\"]").first ();
              this.target$
                  .prop ("title", response.display).val (response.display);
              hidden$.val (response.value);
          }
        }
    );
    $.fn.gtw_e_type_selector_hd = function gtw_e_type_selector_hd (opts) {
        this.each
            ( function () {
                var selector = new ET_Selector_HD (opts);
                var self     = $(this);
                selector.hd_input$ = self;
                self.gtw_hd_input
                    ( { callback       : function (ev) {
                            selector.activate_cb (ev);
                        }
                      , closing_flag   : selector.options.closing_flag
                      , trigger_event  : "click keydown"
                      }
                    );
              }
            );
        return this;
    };
    $.fn.gtw_e_type_selector_hd_mf3 = function gtw_e_type_selector_hd_mf3 (opts) {
        this.each
            ( function () {
                var selector = new ET_Selector_MF3 (opts);
                var self     = $(this);
                selector.hd_input$ = self;
                self.gtw_hd_input
                    ( { callback       : function (ev) {
                          selector.activate_cb (ev)
                        }
                      , clear_callback : function (ev) {
                          selector.clear_cb (ev)
                        }
                      , closing_flag   : selector.options.closing_flag
                      , key_trigger    : {32 : 1, 38 : 1} // space, cursor up
                      , trigger_event  : "click keydown"
                      }
                    );
                self.data ("gtw_e_type_selector_mf3", selector);
              }
            );
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/e_type_selector.js
