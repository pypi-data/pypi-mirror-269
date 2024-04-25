# -*- coding: utf-8 -*-
# Copyright (C) 2015 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package CAL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CAL.ui_display
#
# Purpose
#    Generic function returning a string usable for display in user interface
#
# Revision Dates
#     6-Feb-2015 (CT) Creation
#    ««revision-date»»···
#--

from   _CAL                       import CAL

import _CAL._DTW_

from   _TFL.ui_display            import *

import datetime

@ui_display.add_type (CAL._DTW_, datetime.date, datetime.time, datetime.timedelta)
def _ui_display_date (obj) :
    return str (obj)
# end def _ui_display_date

if __name__ != "__main__" :
    CAL._Export ("ui_display")
### __END__ CAL.ui_display
