# -*- coding: utf-8 -*-
# Copyright (C) 2013 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.MY.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.MY.Sequence
#
# Purpose
#    Emulate a database sequence for mySQL
#
# Revision Dates
#    24-Jun-2013 (CT) Creation
#    26-Aug-2013 (CT) Split into `Sequence`, `Sequence_PID`, `Sequence_X`
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

from   _TFL.pyk   import pyk

import _MOM._DBW
import _MOM._DBW._SAW._MY.DBS
import _MOM._DBW._SAW.Sequence

class _MY_Sequence_ (MOM.DBW.SAW._Sequence_) :
    """Emulate a database sequence for MySQL"""

    _table_kw           = dict \
        ( mysql_engine  = "InnoDB"
        )

# end class _MY_Sequence_

class MY_Sequence (_MY_Sequence_, MOM.DBW.SAW.Sequence) :
    """Emulate a database sequence for MySQL without its own sequence table"""

    _real_name          = "Sequence"

Sequence = MY_Sequence # end class

class MY_Sequence_PID (_MY_Sequence_, MOM.DBW.SAW.Sequence_PID) :
    """Emulate a database sequence for MySQL for `pid`"""

    _real_name          = "Sequence_PID"

Sequence_PID = MY_Sequence_PID # end class

class MY_Sequence_X (_MY_Sequence_, MOM.DBW.SAW.Sequence_X) :
    """Emulate a database sequence for MySQL with its own sequence table"""

    _real_name          = "Sequence_X"

Sequence_X = MY_Sequence_X # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.MY._Export ("*")
### __END__ MOM.DBW.SAW.MY.Sequence
