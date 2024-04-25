/*
** Copyright (C) 2009-2010 Martin Glück All rights reserved
** Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
**
** This module is licensed under the terms of the BSD 3-Clause License
** <https://www.gg32.com/license/bsd_3c.html>.
** ****************************************************************************
**
**++
** Name
**    I18N
**
** Purpose
**    I18N handling for javascript code
**
** Revision Dates
**    27-Feb-2010 (MG) Creation
**    ««revision-date»»···
**--
*/

(function($)
{
  $.I18N =$.I18N || {};
  var plural_pat =
    /^Plural-Forms:\s*nplurals\s*=\s*(\d+);\s*plural\s*=\s*([^a-zA-Z0-9\$]*([a-zA-Z0-9\$]+).+)$/m
  var plural     = function (n) { return n != 1; }
  $.extend
    ( $.I18N
    , { catalogs        : {}
      , lang            : ""
      , plurals         : {}

      , set_catalog : function (language, data)
        {
          $.I18N.catalogs [language] = $.I18N.catalogs [language] || {};
          $.extend ($.I18N.catalogs [language], data);
          /* get the header and try to find the plural function definition */
          var pl = plural_pat.exec ($.I18N.catalogs [language][""]);
          if (pl)
            {

              var expr = pl [2];
              var np   = pl [1];
              var v    = pl [3];
              try
                {
                  var fn = eval
                    ("(function (" + v + ") {return " + expr + ";})");
                }
              catch (e)
                {return;}
              $.I18N.plurals [language] = fn;
            }
          else
              $.I18N.plurals [language] = plural;
          $.I18N.lang                   = language;
        }
      , load            : function (language)
        {
          var $links = $("link[rel=I18N]");
          if (language) $links = $links.filter ("[lang=" + language + "]");
          $links.each (function ()
            {
              $.get (this.href, function (data)
                {
                  $.I18N.set_catalog (langage, data);
                });
            });
        }
        , gettext : function (msgstr)
          {
            var lang = $.I18N.lang;

            if ($.I18N.catalogs [lang] === undefined)
              {
                return msgstr;
              }

            var trans = $.I18N.catalogs [lang] [msgstr];
            if(typeof trans == "string")
              {
                return trans;
              }
            else if (typeof trans == "object" && trans.constructor == Array)
              { // the translation contains plural(s), yet gettext was called
                return trans [0];
              }
            return msgstr;
          }
        , ngettext: function ()
          {
            var lang     = $.I18N.lang;
            var argv     = Array.apply (null, arguments);
            var number   = argv [argv.length - 1];
            var singular = argv [0];
            var plurals  = argv.slice (0, -1);
            var trans    = plurals;

            if ($.I18N.catalogs [lang] != undefined)
              {
                trans = $.I18N.catalogs [lang] [singular];
              }

            if (typeof trans == "string")
              { // called ngettext, but no plural forms available :-?
                return trans;
              }
            else if (typeof trans == "object" && trans.constructor == Array)
              {
                var n = $.I18N.plurals [lang] (umber);
                if (typeof n == "boolean" && plurals.length == 2)
                  {
                    n = n ? 1 : 0;
                  }
                if (typeof n == "number" && n < trans.length)
                  {
                    return trans [n];
                  }
              }
            return singular;
          }
      }
    );
  $.I18N._ = $.I18N._T = $.I18N.gettext;
  $.I18N._Tn           = $.I18N.ngettext;
})(jQuery);
