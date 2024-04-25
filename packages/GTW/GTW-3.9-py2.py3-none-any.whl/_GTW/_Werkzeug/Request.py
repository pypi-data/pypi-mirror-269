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
#    GTW.Werkzeug.Request
#
# Purpose
#    Extend werkzeug's Request class
#
# Revision Dates
#    19-Jun-2012 (CT) Creation
#    29-Jun-2012 (CT) Redefine `json` to add exception handler
#     2-Jul-2012 (CT) Add `has_option`
#     3-Jul-2012 (CT) Redefine `values` to conditionally return `json`
#    31-Jul-2012 (CT) Add `HTTP_Exception`
#    20-Jan-2014 (CT) Add `url_x`
#    13-Mar-2014 (CT) Remove `url_x`
#    28-Aug-2014 (CT) Wrap `safe_str_cmp` to normalize args to `iso-8859-1`
#    21-Oct-2015 (CT) Don't use `werkzeug.contrib.wrappers.JSONRequestMixin`
#                     * because https://github.com/mitsuhiko/werkzeug/issues/731
#                     * raises BadRequest if `self.data` is `bytes` (Python 3)
#                       and simplejson isn't available; without giving a
#                       sensible explanation !!!
#    21-Oct-2015 (CT) Change `body` to run `.data` through `pyk.decoded`
#    30-Mar-2020 (CT) Adapt to werkzeug 1.0
#                     - no werkzeug.contrib.wrappers.DynamicCharsetRequestMixin
#    26-Oct-2022 (CT) Use `hmac.compare_digest`, not werkzeug's `safe_str_cmp`
#                     - werkzeug deprecated that and removed it in 2.0
#    ««revision-date»»···
#--

from   _GTW                       import GTW
from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

import _GTW.Request_Data
import _GTW._Werkzeug

from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.M_Class

from   werkzeug.exceptions           import HTTPException as HTTP_Exception
from   werkzeug.wrappers             import Request

import hmac
import json
import logging

def safe_str_cmp (lhs, rhs) :
    l = pyk.encoded (lhs, "iso-8859-1")
    r = pyk.encoded (rhs, "iso-8859-1")
    return hmac.compare_digest (l, r)
# end def safe_str_cmp

class _WZG_Request_ (Request, metaclass = TFL.Meta.M_Class) :
    """Extend werkzeug's Request class."""

    _real_name           = "Request"

    url_charset          = "utf-8"

    max_content_length   = 1024 * 1024 * 4
    max_form_memory_size = 1024 * 1024 * 2

    @Once_Property
    def body (self) :
        return pyk.decoded (self.data, self.charset)
    # end def body

    @Once_Property
    def path_x (self) :
        query  = self.query_string
        result = self.path
        if query :
            result = "%s?%s" % (result, query)
        return result
    # end def path_x

    @Once_Property
    def json (self) :
        result = {}
        if "json" in self.environ.get ("CONTENT_TYPE", "").lower () :
            try :
                ### For json, encoding should always be utf-8
                body = pyk.decoded (self.data, "utf-8")
            except Exception as exc :
                logging.exception ("*** Json decoding error")
            else :
                try :
                    result = json.loads (body)
                except Exception as exc :
                    pass
        return result
    # end def json

    @Once_Property
    def req_data (self) :
        result = GTW.Request_Data (self.values)
        result.files = self.files
        return result
    # end def req_data

    @Once_Property
    def req_data_list (self) :
        result = GTW.Request_Data_List (self.values)
        result.files = self.files
        return result
    # end def req_data_list

    @Once_Property
    def values (self) :
        result = self.__super.values
        if not result :
            result = self.json
        return result
    # end def values

    def has_option (self, key) :
        return self.req_data.has_option (key)
    # end def get

Request = _WZG_Request_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("Request", "safe_str_cmp", "HTTP_Exception")
### __END__ GTW.Werkzeug.Request
