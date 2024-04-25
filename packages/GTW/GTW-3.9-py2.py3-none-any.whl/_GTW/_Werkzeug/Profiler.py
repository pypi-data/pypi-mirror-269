# -*- coding: utf-8 -*-
# Copyright (C) 2012-2020 Christian Tanzer All rights reserved
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
#    GTW.Werkzeug.Profiler
#
# Purpose
#    Profiler for werkzeug-based WSGI applications
#
# Revision Dates
#    20-Jun-2012 (CT) Factor from `GTW.Werkzeug.Application`
#    30-Mar-2020 (CT) Adapt to werkzeug 1.0
#                     - no werkzeug.contrib.profiler
#                     - no werkzeug.middleware.profiler.MergeStream
#    ««revision-date»»···
#--

from   _GTW                      import GTW
from   _TFL                      import TFL

import _GTW._Werkzeug

import _TFL._Meta.Object

from   werkzeug.middleware.profiler import ProfilerMiddleware

import sys

class Profiler (TFL.Meta.Object) :
    """Profiler for werkzeug-based WSGI applications."""

    def __init__ \
            ( self
            , restrictions = ()
            , sort_by      = ('time', 'calls')
            ) :
        self.restrictions  = restrictions
        self.sort_by       = sort_by
    # end def __init__

    def __call__ (self, app, stream = sys.stdout) :
        return ProfilerMiddleware (app, stream, self.sort_by, self.restrictions)
    # end def __call__

# end class Profiler

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Profiler
