# -*- coding: utf-8 -*-
# Copyright (C) 2015 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.UI_Spec
#
# Purpose
#    UI specification for E_Types defined by MOM
#
# Revision Dates
#    16-Dec-2015 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                     import MOM
from   _TFL                     import TFL

import _TFL.Sorted_By

class UI_Spec (object) :
    """UI specification for E_Types defined by MOM."""

    Document              = dict \
        ( list_display    = ("entity", "url", "type")
        )

    Id_Entity_has_Tag     = dict \
        (
        )

    Tag                   = dict \
        ( list_display    = ("name", "description")
        )

# end class UI_Spec

if __name__ != "__main__" :
    MOM._Export ("UI_Spec")
### __END__ MOM.UI_Spec
