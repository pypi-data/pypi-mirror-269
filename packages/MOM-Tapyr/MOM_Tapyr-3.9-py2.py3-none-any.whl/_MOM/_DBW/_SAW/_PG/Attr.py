# -*- coding: utf-8 -*-
# Copyright (C) 2016 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.PG.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.PG.Attr
#
# Purpose
#    PostgreSQL specific attribute handling for SAW
#
# Revision Dates
#    14-Sep-2016 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL
from   _TFL.pyk            import pyk

from   _MOM._DBW._SAW      import SAW, SA

import _MOM._DBW._SAW.Attr
import _MOM._DBW._SAW._PG

if __name__ != "__main__" :
    MOM.DBW.SAW.PG._Export_Module ()
### __END__ MOM.DBW.SAW.PG.Attr
