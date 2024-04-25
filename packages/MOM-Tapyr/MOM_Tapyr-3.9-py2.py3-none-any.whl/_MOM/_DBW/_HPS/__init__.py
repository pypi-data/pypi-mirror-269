# -*- coding: utf-8 -*-
# Copyright (C) 1999-2010 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package _MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.HPS.__init__
#
# Purpose
#    Database wrapper for Hash-Pickle-Store
#
# Revision Dates
#    18-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM._DBW              import DBW
from   _TFL.Package_Namespace import Package_Namespace

HPS = Package_Namespace ()
DBW._Export ("HPS")

del Package_Namespace

### __END__ MOM.DBW.HPS.__init__
