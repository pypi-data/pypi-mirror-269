// Copyright (C) 2016 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/ajax.js
//
// Purpose
//    Vanilla javascript function doing AJAX requests
//
// Revision Dates
//    26-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.ajax = $.merge
        ( function ajax (opts) {
            var O            = $.merge ({}, ajax.defaults, opts);
            var Hs           = $.merge ({}, ajax.defaults.headers, O.headers);
            var body;
            var data         = O.data;
            var typ          = O.typ.toUpperCase;
            var url          = new URL (O.url, location);
            var xhr          = new XMLHttpRequest ();
            var body_allowed = typ !== "GET";
            var json_type    = Hs ["Content-Type"] === "application/json";
            function error_cb (ev) {
                var msg, status = xhr.statusText || "Network Error";
                if (O.error) {
                    O.error (xhr, status, ev);
                } else {
                    msg = typ + " request to " + url + " failed: " + status;
                    $.error (msg, "\n", xhr, "\n", Hs, "\n", ev);
                };
            };
            function success_cb (ev) {
                var status = xhr.status;
                var type   = xhr.getResponseHeader ("Content-Type");
                var body   = xhr.responseText;
                if (! /^(0|2\d{2}|304)$/.test (status)) {
                    error_cb (ev);
                } else {
                    if (type === "application/json") {
                        try {
                            body = JSON.parse (body);
                        }  catch (e) {
                            body = { error : e };
                        };
                    };
                    if (O.success) {
                        O.success (body, xhr.statusText, xhr);
                    };
                };
            };
            if (data) {
                if (typeof data !== "string") {
                    if (body_allowed && json_type) {
                        data = JSON.stringify    (data);
                    } else {
                        data = $.form_urlencoded (data);
                    };
                };
                if (body_allowed) {
                    body = data;
                } else {
                    url.search += data;
                };
            };
            xhr.open (typ, url, O.async, O.username, O.password);
            for (var header in Hs) {
                xhr.setRequestHeader (header, Hs [header]);
            };
            xhr.timeout = O.timeout;
            $.bind (xhr, "abort error timeout", error_cb);
            $.bind (xhr, "load", success_cb);
            xhr.send (body);
            return xhr;
          }
        , defaults :
            { async       : true
            , data        : ""
            , dataType    : "json"
            , headers     :
                { "Content-Type" : "application/json"
                }
            , timeout     : 0
            , type        : "GET"
            , url         : ""
            }
        );
  } ($V5a)
);

// __END__ V5a/ajax.js
