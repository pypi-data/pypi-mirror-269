// Copyright (C) 2011-2014 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW_inspect
//
// Purpose
//    Provide functions to inspect Javascript objects
//
// Revision Dates
//    28-Jan-2011 (CT) Creation
//     9-Mar-2011 (CT) `copy` added
//    31-May-2011 (MG) Missing `var` added
//    29-Apr-2013 (CT) Add `show1`
//    20-Jan-2014 (CT) Add missing `lev` to `show1`
//     1-May-2014 (CT) Change `show` to just return strings
//    18-Jun-2014 (CT) Add `update_transitive`
//    ««revision-date»»···
//--

( function () {
    "use strict";

    var inspect;
    var blanks =
    "                                                                         ";
    $GTW.inspect = inspect = new $GTW.Module (
        { blanks : blanks
        , copy : function copy (obj, filter) {
              var i, l, k, v;
              var keys = inspect.keys (obj, filter);
              var result = {};
              if (obj.constructor !== {}.constructor) {
                  result.constructor = obj.constructor;
              }
              for (i = 0, l = keys.length; i < l; i += 1) {
                  k = keys [i];
                  result [k] = obj [k];
              }
              return result;
          }
        , filter_function  : function filter_function (name, obj) {
              return typeof (obj [name]) === "function";
          }
        , filter_not_function : function filter_not_function (name, obj) {
              return typeof (obj [name]) !== "function";
          }
        , filter_object : function filter_object (name, obj) {
              return typeof (obj [name]) === "object";
          }
        , filter_own : function filter_own (name, obj) {
              return obj.hasOwnProperty (name);
          }
        , key_cmp : function key_cmp (l, r) {
              if (typeof l === "string") { l = l.toLowerCase (); }
              if (typeof r === "string") { r = r.toLowerCase (); }
              if      (l <   r) { return -1; }
              else if (l === r) { return  0; }
              else              { return +1; }
          }
        , keys : function keys (obj, filter) {
              var result = [];
              var name;
              if (filter === undefined) {
                  filter = inspect.filter_own;
              }
              for (name in obj) {
                  if (filter (name, obj)) {
                      result.push (name);
                  }
              }
              return result;
          }
        , items : function items (obj, filter) {
              var result = [];
              var name;
              if (filter === undefined) {
                  filter = inspect.filter_own;
              }
              for (name in obj) {
                  if (filter (name, obj)) {
                      result.push ([name, obj [name]]);
                  }
              }
              return result;
          }
        , show : function show (obj, filter, level, top_filter) {
              var i, l, name, r, regexp, value;
              var result = [];
              var lev    = level || 0;
              var indent = blanks.slice (0, 4 * lev);
              var names;
              if (typeof obj == "string") {
                  return obj;
              };
              names = inspect.keys (obj, top_filter || filter).sort (inspect.key_cmp);
              for (i = 0, l = names.length; i < l; i += 1) {
                  name  = names [i];
                  value = obj   [name];
                  switch (typeof value) {
                      case "function" :
                          value  = value.toString ();
                          regexp = new RegExp ("function +" + name + " *\\(");
                          if (value.match (regexp)) {
                              r = indent + value;
                          } else {
                              r = indent + name + " : " + value;
                          };
                          r = r.split ("\n") [0].replace (/ *\{ *$/, "");
                          break;
                      case "object" :
                          result.push (indent + name + " :");
                          r = inspect.show (value, filter, lev + 1);
                          break;
                      case "string" :
                          r = indent + name + " = \"" + value + "\"";
                          break;
                      default :
                          r = indent + name + " = " + value;
                  };
                  result.push (r);
              };
              return result.join ("\n");
          }
        , show1  : function show1 (value, filter, level, top_filter) {
              var result;
              var rs  = [];
              var lev = level || 0;
              switch (typeof value) {
                  case "function" :
                      result = value.toString ();
                      break;
                  case "object" :
                      if (value) {
                          if (value.constructor == Array) {
                              l = value.length;
                              for (i = 0; i < l; i += 1) {
                                  rs.push (show1 (value [i], filter, lev + 1));
                              };
                              result = "[" + rs.join (",") + "]";
                          } else {
                              result = inspect.show
                                  (value, filter, lev + 1, top_filter);
                          }
                      };
                      break;
                  default :
                      result = value;
              };
              return result;
          }
        , update_transitive : function update_transitive (self, other) {
              var k, v;
              for (k in other) {
                  if (other.hasOwnProperty (k)) {
                      v = other [k];
                      if  (  (typeof v === "object")
                          && (v.constructor !== Array)
                          && (k in self)
                          ) {
                          inspect.update_transitive (self [k], v);
                      } else {
                          self [k] = v;
                      };
                  };
              };
          }
        , values : function values (obj, filter) {
              var result = [];
              var name;
              if (filter === undefined) {
                  filter = inspect.filter_own;
              }
              for (name in obj) {
                  if (filter (name, obj)) {
                      result.push (obj [name]);
                  }
              }
              return result;
          }
        }
    );
  } ()
);

// __END__ GTW_inspect.js
