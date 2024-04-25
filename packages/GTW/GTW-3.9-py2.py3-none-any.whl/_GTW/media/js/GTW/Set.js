// Copyright (C) 2011-2014 Christian Tanzer All rights reserved
// tanzer@gg32.com                                      https://www.gg32.com
// #*** <License> ************************************************************#
// This script is licensed under the terms of the BSD 3-Clause License
// <https://www.gg32.com/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/Set
//
// Purpose
//    Provide a javascript class modelling a Set, i.e., an unordered set of
//    unique elements
//
// Revision Dates
//    10-Mar-2011 (CT) Creation
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    ««revision-date»»···
//--

( function () {
    "use strict";

    var _ = {}, hasOwnProperty = _.hasOwnProperty, token = {};
    var Set = $GTW.Class.extend (
        { init : function init () {
              this.update.apply (this, arguments);
          }
        , add : function add (arg) {
              this [arg] = token;
              return this;
          }
        , clear : function clear () {
              var keys = this.elements ();
              for (var i = 0, li = keys.length, k; i < li; i++) {
                  k = keys [i];
                  delete this [k];
              }
          }
        , contains : function contains (arg) {
              var elem = this [arg];
              return elem && elem === token;
          }
        , copy : function copy () {
              var result = new Set ();
              result.union_update (this);
              return result;
          }
        , difference : function difference (other) {
              var result = this.copy ();
              result.difference_update (other);
              return result;
          }
        , difference_update : function difference_update (other) {
              var keys = other.elements ();
              for (var i = 0, li = keys.length, k; i < li; i++) {
                  k = keys [i];
                  if (this.contains (k)) {
                      delete this [k];
                  }
              }
              return this;
          }
        , discard : function discard (arg) {
              delete this [arg];
              return this;
          }
        , elements : function elements () {
              return $GTW.inspect.keys
                  ( this
                  , function (name, obj) { return obj [name] === token; }
                  );
          }
        , intersection : function intersection (other) {
              var result = this.copy ();
              result.intersection_update (other);
              return result;
          }
        , intersection_update : function intersection_update (other) {
              var keys = this.elements ();
              for (var i = 0, li = keys.length, k; i < li; i++) {
                  k = keys [i];
                  if (! other.contains (k)) {
                      delete this [k];
                  }
              }
              return this;
          }
        , is_disjoint : function is_disjoint (other) {
              return this.intersection (other).size () === 0;
          }
        , is_subset : function is_subset (other) {
              var keys = this.elements ();
              for (var i = 0, li = keys.length, k; i < li; i++) {
                  k = keys [i];
                  if (! other.contains (k)) {
                      return false;
                  }
              }
              return true;
          }
        , is_superset : function is_superset (other) {
              return other.is_subset (this);
          }
        , remove : function remove (arg) {
              if (this.contains (arg)) {
                  delete this [arg];
              } else {
                  throw new Error
                      ("Set '" + this.elements () + "' doesn't contain " + arg);
              }
              return this;
          }
        , size : function size () {
              return this.elements ().length;
          }
        , symmetric_difference : function symmetric_difference (other) {
              var result = this.copy ();
              result.symmetric_difference_update (other);
              return result;
          }
        , symmetric_difference_update : function symmetric_difference_update (other) {
              var section = this.intersection (other);
              this.union_update (other).difference_update (section);
              return this;
          }
        , union : function union (other) {
              var result = this.copy ();
              result.union_update (other);
              return result;
          }
        , union_update : function union_update (other) {
              this.update.apply (this, other.elements ());
              return this;
          }
        , update : function update () {
              for (var i = 0, li = arguments.length, arg; i < li; i++) {
                  arg = arguments [i];
                  this [arg] = token;
              }
              return this;
          }
        }
    );
    $GTW.Set = Set;
  } ()
);

// __END__ GTW/Set.js
