# -*- coding: utf-8 -*-
# Copyright (C) 2009 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.__init__
#
# Purpose
#    Package defining Object Model Parts
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

OMP = Package_Namespace ()
GTW._Export ("OMP")

del Package_Namespace

### __END__ GTW.OMP.__init__
