# -*- coding: utf-8 -*-
# Copyright (C) 2010-2016 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Attr_Type
#
# Purpose
#    Define attribute types for package GTW.OMP.PAP
#
# Revision Dates
#     4-Jun-2010 (CT) Creation
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    14-May-2012 (CT) Add `A_Sex.P_Type`
#     7-Feb-2016 (CT) Modernize
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Named_Object_

import _GTW._OMP._PAP

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.pyk                 import pyk

class A_Sex (_A_Named_Object_) :
    """Sex of a person."""

    example   = "F"
    typ       = "Sex"
    P_Type    = str
    Table     = \
        { "F"  : _("Female")
        , "M"  : _("Male")
        }

# end class A_Sex

__attr_types = Attr.attr_types_of_module ()
__all__      = __attr_types

if __name__ != "__main__" :
    GTW.OMP.PAP._Export (* __all__)
### __END__ GTW.OMP.PAP.Attr_Type
