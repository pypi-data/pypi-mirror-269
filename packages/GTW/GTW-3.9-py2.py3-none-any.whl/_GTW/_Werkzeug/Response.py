# -*- coding: utf-8 -*-
# Copyright (C) 2012-2022 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.Werkzeug.Response
#
# Purpose
#    Extend werkzeug's Response class
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#     2-Mar-2013 (CT) Add `add_header` and `set_header` (both encode `key`)
#    14-Mar-2014 (CT) Add `encoded_url`
#    13-Apr-2015 (CT) Use `TFL.json_dump.default`
#     6-May-2015 (CT) Use `TFL.json_dump.to_string`
#    21-Oct-2015 (CT) Use `as_str`, node `encoded`, for header `key`
#    30-Mar-2020 (CT) Adapt to werkzeug 1.0
#                     - no werkzeug.contrib.wrappers.DynamicCharsetResponseMixin
#    26-Oct-2022 (CT) Use `url_encode`, not `Href`, for `encoded_url`
#    ««revision-date»»···
#--

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._Werkzeug

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.pyk                   import pyk

import _TFL._Meta.M_Class
import _TFL.json_dump

from   werkzeug.wrappers          import Response
from   werkzeug.urls              import url_encode

class _WZG_Response_ ( Response, metaclass = TFL.Meta.M_Class) :
    """Extend werkzeug's Response class."""

    _real_name           = "Response"

    default_charset      = "utf-8"

    def add_header (self, key, value, ** kw) :
        key = pyk.as_str (key, "ascii")
        return self.headers.add (key, value, ** kw)
    # end def add_header

    def clear (self) :
        self.headers.clear ()
        self.response = []
        self.status   = self.default_status
    # end def clear

    def encoded_url (self, * args, ** kw) :
        if args :
            raise NotImplementedError ("encoded_url with `* args`")
            ### This used to be implemented on top of werkzeug.urls.Href which
            ### was removed in werkzeug 2.1
            ###
            ### As it wasn't used in GTW, I didn't bother
            result = Href (args [0])
            return result (* args [1:], ** kw)
        else :
            result = "?" + url_encode (kw)
            return result
    # end def encoded_url

    def write (self, data) :
        self.response.append (data)
    # end def write

    def set_header (self, key, value, ** kw) :
        key = pyk.as_str (key, "ascii")
        return self.headers.set (key, value, ** kw)
    # end def set_header

    def write_json (self, __data = None, ** kw) :
        data = dict (kw)
        if __data is not None :
            data.update (__data)
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (TFL.json_dump.to_string (data))
    # end def write_json

Response = _WZG_Response_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("Response")
### __END__ GTW.Werkzeug.Response
