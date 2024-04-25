# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package GTW.OMP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.NET.__init__
#
# Purpose
#    Package defining a partial object model for network objects
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    15-Jun-2013 (CT) Use `MOM.Derived_PNS`
#    ««revision-date»»···
#--

from   _GTW._OMP              import OMP
from   _MOM                   import MOM
import _MOM.Derived_PNS

_desc_ = __doc__ = """
Partial object model for network objects.
"""

NET = MOM.Derived_PNS (parent = MOM)
OMP._Export ("NET")

### __END__ GTW.OMP.NET.__init__
