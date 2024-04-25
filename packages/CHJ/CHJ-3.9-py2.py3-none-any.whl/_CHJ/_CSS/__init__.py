# -*- coding: utf-8 -*-
# Copyright (C) 2007-2016 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package CHJ.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CHJ.CSS.__init__
#
# Purpose
#    Model cascading style sheets
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#    11-Oct-2016 (CT) Move from `GTW` to `CHJ`
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _CHJ                   import CHJ

CSS = Package_Namespace ()
CHJ._Export ("CSS")

del Package_Namespace

### __END__ CHJ.CSS.__init__
