# -*- coding: utf-8 -*-
# Copyright (C) 2012-2022 Christian Tanzer All rights reserved
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
#    CAL.date_time_localizer
#
# Purpose
#    Convert date-times given with tzoffset into local time without tzoffset
#
# Revision Dates
#    30-Mar-2012 (CT) Creation
#    18-Apr-2012 (CT) Use `I18N.decode` and `pyk.fprint`
#    11-Jul-2018 (CT) Quote `[`, `]` inside character groups of regexpes
#                     + Python 3.7 gives `FutureWarning: Possible nested set`
#                       otherwise (https://bugs.python.org/issue30349)
#    19-Aug-2019 (CT) Use `print_prepr`
#     6-Oct-2022 (CT) Add `timezone_context`; use it to fix tz-specific tests
#    ««revision-date»»···
#--

from   _TFL                import TFL
from   _CAL                import CAL

from   _TFL.Regexp         import Regexp, Multi_Re_Replacer, Re_Replacer, re
from   _TFL.portable_repr  import print_prepr
from   _TFL.pyk            import pyk

import _CAL.Date_Time
import _TFL.CAO
import _TFL.I18N

import os
import time

date_time_localizer_pattern = Regexp \
    ( ( r"(?P<head> ^|[\[(\s])"
        r"(?P<year>  \d{4,4})"
        r"([-/]?)"
        r"(?P<month> \d{2,2})"
        r"\3"
        r"(?P<day>   \d{2,2})"
        r"[T ]"
      )
    + CAL.Date_Time.time_pattern.pattern
    + r"(?P<tail> $|[\])\s])"
    , flags = re.VERBOSE | re.IGNORECASE
    )
_cleaned = Multi_Re_Replacer \
    ( Re_Replacer (r"^[\[(\s]", "")
    , Re_Replacer (r"[\])\s]$", "")
    )

def date_time_localizer \
        (s, format = "%Y-%m-%d %H:%M", pattern = None, count = 0) :
    """Convert date-times in `s` into local time without tzoffset.

    >>> with timezone_context ("CET") :
    ...   print_prepr (date_time_localizer ("09d82ac 2012-03-29 21:06:26 +0200 martin@mangari.org"))
    ...   print_prepr (date_time_localizer ("f6baffa [2012-03-29 10:06:46 -0400] martin@mangari.org"))
    ...   print_prepr (date_time_localizer ("f99a29d (2005-03-22 09:34:40 +0000) tanzer@swing.co.at"))
    '09d82ac 2012-03-29 21:06 martin@mangari.org'
    'f6baffa [2012-03-29 16:06] martin@mangari.org'
    'f99a29d (2005-03-22 10:34) tanzer@swing.co.at'

    """
    if pattern is None :
        pattern = date_time_localizer_pattern
    def repl (match) :
        value  = _cleaned (match.group (0))
        local  = CAL.Date_Time.from_string (value).as_local ()
        result = "%s%s%s" % \
            ( match.group     ("head")
            , local.formatted (format)
            , match.group     ("tail")
            )
        return result
    return pattern.sub (repl, s, count)
# end def date_time_localizer

@TFL.Contextmanager
def timezone_context (tzname) :
    """Temporarily change the local timezone to `tzname`."""
    old_tzname = time.tzname [0]
    try :
        os.environ ["TZ"] = tzname
        time.tzset  ()
        yield
    finally :
        os.environ ["TZ"] = old_tzname
        time.tzset  ()
# end def timezone_context

def _main (cmd) :
    import fileinput
    lines = fileinput.input (cmd.argv)
    if cmd.output :
        sys.stdout = open (cmd.output, "a")
    for l in lines :
        if isinstance (l, str) :
            l = TFL.I18N.decode (l)
        ll = date_time_localizer (l, cmd.format)
        try :
            print (ll, end = "")
        except IOError :
            import sys
            sys.exit (0)
    print ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "file:P?Files to convert times for (default: stdin)"
        ,
        )
    , opts          =
        ( "-format:S=%Y-%m-%d %H:%M"
            "?Output format for converted date-time values"
        , "-output:S?Name of file to which to write output (default: stdout)"
        )
    , min_args      = 0
    , description   =
        "Convert date-times in input into local time without tzoffset"
    )

if __name__ != "__main__" :
    CAL._Export ("*")
if __name__ == "__main__" :
    _Command ()
### __END__ CAL.date_time_localizer
