# -*- coding: utf-8 -*-
# Copyright (C) 2012 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.PAP.Nickname
#
# Purpose
#    Model nickname of a subject
#
# Revision Dates
#    12-Sep-2012 (RS) Creation
#    11-Oct-2012 (RS) Move here from `FFM`, Nickname of `Subject` not `Person`
#    12-Oct-2012 (RS) Don't `ignore_case`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Property

_Ancestor_Essence = PAP.Property

class _PAP_Nickname_ (_Ancestor_Essence) :
    """Nickname of a subject"""

    _real_name = "Nickname"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class name (A_String) :
            """The nickname."""

            kind           = Attr.Primary
            max_length     = 32
            rank           = 1

            completer      = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class left

    # end class _Attributes

Nickname = _PAP_Nickname_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Nickname
