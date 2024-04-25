# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Christian Tanzer All rights reserved
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
#    GTW.OMP.EVT.__init__
#
# Purpose
#    Package defining a partial object model for calendary events
#
# Revision Dates
#    10-Mar-2010 (CT) Creation
#     9-Oct-2012 (CT) Add `_desc_`
#    15-Jun-2013 (CT) Use `MOM.Derived_PNS`
#    ««revision-date»»···
#--

from   _GTW._OMP              import OMP
from   _MOM                   import MOM
import _MOM.Derived_PNS

_desc_ = __doc__ = """
Partial object model for calendary events.
"""

EVT = MOM.Derived_PNS (parent = MOM, pns_alias = "EVT")
OMP._Export ("EVT")

### __END__ GTW.OMP.EVT.__init__
