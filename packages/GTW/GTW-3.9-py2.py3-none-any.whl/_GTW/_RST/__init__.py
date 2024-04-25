# -*- coding: utf-8 -*-
# Copyright (C) 2012 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.RST.__init__
#
# Purpose
#    Framework for RESTful web services
#
# Revision Dates
#     6-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

RST = Package_Namespace ()
GTW._Export ("RST")

del Package_Namespace

### __END__ GTW.RST.__init__
