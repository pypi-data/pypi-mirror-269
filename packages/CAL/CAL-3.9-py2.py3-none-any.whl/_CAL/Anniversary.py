# -*- coding: utf-8 -*-
# Copyright (C) 2020-2024 Christian Tanzer All rights reserved
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
#    CAL.Anniversary
#
# Purpose
#    Model anniversaries
#
# Revision Dates
#    21-May-2020 (CT) Creation
#    11-Apr-2022 (CT) Fix `_Anniversary_Day_.description`
#    27-Feb-2024 (CT) Add `Wedding.symbol`
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL
from   _TFL.pyk                 import pyk

from   _TFL.I18N                import _, _T, _Tn

import _CAL.Date
import _CAL.Day_Rule
import _CAL.Delta

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property

class _Anniversary_Day_ (CAL.Day_Rule._Ruled_Day_) :
    """Anniversary day in a specific year."""

    anniversary = TFL.Meta.Alias_Property ("_rule")

    @TFL.Meta.Once_Property
    def age (self) :
        result = self._date.year - self.anniversary.year
        return result if result else self.anniversary.symbol
    # end def age

    @TFL.Meta.Once_Property
    def day_abbr (self) :
        return "%s : %s" % (self.anniversary.abbr, self.age)
    # end def day_abbr

    @property
    def desc (self) :
        return self.anniversary.abbr
    # end def desc

    @TFL.Meta.Once_Property
    def description (self) :
        age = self.age
        if isinstance (age, int) :
            result = "%s %s %s" % (self.desc, age, _Tn ("year", "years", age))
        else :
            result = self.desc
        return result
    # end def description

    @TFL.Meta.Once_Property
    def event_abbr (self) :
        return "%s:%2s" % (self.wk_day_abbr [:2], self.age)
    # end def event_abbr

# end class _Anniversary_Day_

class Anniversary (CAL.Day_Rule.Fixed) :
    """Day where an event happened that started an anniversary."""

    _abbr           = None
    _Day_of_Year    = _Anniversary_Day_

    symbol          = "\u2606" ### star white

    def __init__ (self, name, year, month, day, delta = None, ** kwds) :
        self._start_date    = CAL.Date (year, month, day)
        self.pop_to_self      (kwds, "abbr", prefix = "_")
        yf = lambda y : y >= year
        self.__super.__init__ \
            (name, month, day, delta = delta, y_filter = yf, ** kwds)
    # end def __init__

    @TFL.Meta.Once_Property
    def abbr (self) :
        return (self._abbr or self.name) + " " + self.symbol
    # end def abbr

    @property
    def year (self) :
        return self._start_date.year
    # end def year

# end class Anniversary

class Birthday (Anniversary) :
    """Day when a person was born."""

    symbol      = "\u2605" ### black_star

# end class Birthday

class Obit (Anniversary) :
    """Day when a person died."""

    symbol      = "\u2020" ### dagger

# end class Obit

class Wedding (Anniversary) :
    """Day when two persons where married."""

    symbol      = "\u26ad" ### marriage_symbol

    def __init__ (self, n1, n2, * args, ** kwds) :
        self.n1 = n1
        self.n2 = n2
        name    = "(%s & %s)" % (n1, n2)
        self.__super.__init__ (name, * args, ** kwds)
    # end def __init__

# end class Wedding

class Anniversaries (CAL.Day_Rule.Set) :

    A = Anniversary
    B = Birthday
    O = Obit
    W = Wedding

# end class Anniversaries

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Anniversary
