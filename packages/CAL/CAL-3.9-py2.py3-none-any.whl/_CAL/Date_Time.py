# -*- coding: utf-8 -*-
# Copyright (C) 2004-2024 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.Date_Time
#
# Purpose
#    Wrapper around `datetime.datetime`
#
# Revision Dates
#    15-Oct-2004 (CT) Creation
#    17-Oct-2004 (CT) Adapted to changes in `_DTW_` and `Delta`
#    28-Dec-2005 (MG) Static method `from_ical` added
#    30-Nov-2006 (CT) `__getattr__` for `CJD`, `MJD`, `TJD`, "CJS", "MJS",
#                     and "TJS" added
#    10-Dec-2006 (CT) `from_julian` added
#    11-Dec-2006 (CT) `from_julian` corrected
#    11-Dec-2006 (CT) `__getattr__` changed to `setattr` the modified value
#    11-Nov-2007 (CT) `sidereal_time` added
#     3-Jan-2008 (CT) `time_pattern` added and `_from_string_match_kw` redefined
#     7-Jan-2008 (CT) `as_utc` added
#    31-Mar-2008 (CT) `combine` added
#    16-Jun-2010 (CT) s/print/pyk.fprint/
#    29-Mar-2012 (CT) Add support for `tzinfo`; factor `as_local`; use
#                     `CAL.Time._from_string_match_kw`
#    15-Sep-2014 (CT) Add `_Date_Time_Arg_` to `CAO` as `[Arg|Opt].Date_Time`
#    19-Sep-2014 (CT) Add `from_string_x`
#     6-May-2015 (CT) Add tests for `jsonified`
#    29-Mar-2016 (CT) Derive `_Date_Time_Arg_` from `CAO.Opt.Date`, not `.Str`
#    21-Apr-2016 (CT) Add check for tail to `_from_string_match_kw`
#    21-Apr-2016 (CT) Redefine `from_string` to pass `check_tail=False`
#    26-Sep-2016 (CT) Add `as_date`, `as_time`
#    26-Sep-2016 (CT) Move `sidereal_time` to `CAL.Sky.Earth`
#     1-Nov-2020 (CT) Make space before `time_pattern.tzinfo` optional
#     5-Oct-2022 (CT) Add `_default_format`
#     6-Oct-2022 (CT) Add `midnight`, `noon`
#     6-Oct-2022 (CT) Use `timezone_context` to fix tz-specific doctests
#     9-Oct-2022 (CT) Simplify `as_local` (support only Python 3.9+)
#    10-Oct-2022 (CT) Add property `yyyy_mm_dd_HH_MM`
#    12-Oct-2022 (CT) Add doctest for `formatted`
#     4-Dec-2022 (CT) Add `JT` (time of day as decimal fraction)
#     4-Dec-2022 (CT) Add `dst_adjustment`
#                     + Add optional argument `tz` to `as_local`
#    18-Oct-2023 (CT) Add `datetime_utcnow`
#                     * drop-in replacement for `datetime.utcnow`
#                     * `datetime.utcnow` deprecated as of Python 3.12
#    29-Feb-2024 (CT) Add `_Command`
#                     + Define `_CAL_Type` as lass/instance property to
#                       return `CAL.Date_Time` (avoid `__main__.Date_Time`)
#    29-Feb-2024 (CT) Add option `-relative_delta`
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _CAL                     import CAL

import _CAL.Date
import _CAL.Time

from   _TFL._Meta.Once_Property import \
    Once_Property, Class_and_Instance_Once_Property
import _TFL.CAO
from   _TFL.pyk                 import pyk
from   _TFL.Regexp              import *

import datetime

class Date_Time (CAL.Date, CAL.Time) :
    """Model a (gregorian) date plus time.

       >>> from _CAL.Delta import Date_Time_Delta as Delta
       >>> from _TFL.json_dump import to_string as jsonified
       >>> from _CAL.date_time_localizer import timezone_context

       >>> d = Date_Time (2004, 10, 15, 16,  3, 14)
       >>> print (d)
       2004-10-15 16:03:14
       >>> print (d.formatted ())
       2004-10-15 16:03:14
       >>> print (d.formatted ("%b"))
       Oct
       >>> print (jsonified ([d, Delta (3)]))
       ["2004-10-15T16:03:14", "3 days, 0:00:00"]

       >>> d.year, d.month, d.day, d.datetime, d.week, d.weekday, d.ordinal
       (2004, 10, 15, datetime.datetime(2004, 10, 15, 16, 3, 14), 42, 4, 731869)
       >>> d.month_name
       'Oct'
       >>> d = d - Delta (3)
       >>> d.year, d.month, d.day, d.datetime, d.week, d.weekday, d.ordinal
       (2004, 10, 12, datetime.datetime(2004, 10, 12, 16, 3, 14), 42, 1, 731866)
       >>> d = d - 1
       >>> d.year, d.month, d.day, d.datetime, d.week, d.weekday, d.ordinal
       (2004, 10, 11, datetime.datetime(2004, 10, 11, 16, 3, 14), 42, 0, 731865)
       >>> d1 = d2 = Date_Time (2004, 10, 15, 16,  3, 14)
       >>> id (d1) == id (d2)
       True
       >>> d1 += 1
       >>> id (d1) == id (d2)
       False
       >>> print (d2 - d1)
       -1 day, 0:00:00

       >>> d = Date_Time (2006, 12, 10, 12, 26, 30)
       >>> print (jsonified ([d1, d, d - d1]))
       ["2004-10-16T16:03:14", "2006-12-10T12:26:30", "784 days, 20:23:16"]

       >>> d.TJD, d.TJS
       (14079.518402777778, 1216470390)
       >>> d
       Date_Time (2006, 12, 10, 12, 26, 30, 0)
       >>> Date_Time.from_julian (14079, kind = "TJD")
       Date_Time (2006, 12, 10, 0, 0, 0, 0)
       >>> Date_Time.from_julian (14079.518402777778, kind = "TJD")
       Date_Time (2006, 12, 10, 12, 26, 30, 0)
       >>> Date_Time.from_julian (1216470390, kind = "TJS")
       Date_Time (2006, 12, 10, 12, 26, 30, 0)

       >>> Date_Time (1988,6,19,12).JD
       2447332.0
       >>> Date_Time (1988,1,27).JD
       2447187.5
       >>> Date_Time (1999,1,1).JD
       2451179.5
       >>> Date_Time (1999,1,1,12).JD
       2451180.0
       >>> Date_Time (2000,1,1,12).JD
       2451545.0

        >>> dt = Date_Time (2022, 12, 4, 12)
        >>> print (dt, dt.JD2000, dt.JT)
        2022-12-04 12:00:00 8373.0 0.0

        >>> dt_mn = dt + 0.5
        >>> print (dt_mn, dt_mn.JD2000, dt_mn.JT)
        2022-12-05 00:00:00 8373.5 0.5

        >>> dt_xx = dt + 0.95
        >>> print (dt_xx, "%.2f" % dt_xx.JD2000, "%.2f" % dt_xx.JT)
        2022-12-05 10:48:00 8373.95 0.95

       >>> with timezone_context ("CET") :
       ...   dt1 = Date_Time (2008, 1, 7, 10, 16, 42, 0)
       ...   dt1
       ...   dt1.as_local ()
       ...   dt1.as_utc ()
       ...   dt2 = Date_Time (2008, 4, 7, 10, 16, 42, 0)
       ...   dt2
       ...   dt2.as_local ()
       ...   dt2.as_utc ()
       ...   dt3 = Date_Time.from_string ("2012-03-29 10:06:46 -0400")
       ...   dt3
       ...   dt3.as_local ()
       ...   dt3.as_utc ()
       Date_Time (2008, 1, 7, 10, 16, 42, 0)
       Date_Time (2008, 1, 7, 10, 16, 42, 0)
       Date_Time (2008, 1, 7, 9, 16, 42, 0)
       Date_Time (2008, 4, 7, 10, 16, 42, 0)
       Date_Time (2008, 4, 7, 10, 16, 42, 0)
       Date_Time (2008, 4, 7, 8, 16, 42, 0)
       Date_Time (2012, 3, 29, 10, 6, 46, 0)
       Date_Time (2012, 3, 29, 16, 6, 46, 0)
       Date_Time (2012, 3, 29, 14, 6, 46, 0)

       >>> print (Date_Time.from_string ("2022 09:42"))
       2022-01-01 09:42:00

       >>> td = Date_Time (2014, 9, 19, 17, 23, 42)
       >>> tt = CAL.Time  (17, 23, 42)

       >>> print (jsonified ((td, tt)))
       ["2014-09-19T17:23:42", "17:23:42"]

       >>> Date_Time.from_string_x ("2017/09/19 17:42:23")
       Date_Time (2017, 9, 19, 17, 42, 23, 0)

       >>> td
       Date_Time (2014, 9, 19, 17, 23, 42, 0)

       >>> tt
       Time (17, 23, 42, 0)

       >>> Date_Time.from_string_x ("+15m", date = td)
       Date_Time (2014, 9, 19, 17, 38, 42, 0)

       >>> Date_Time.from_string_x ("+3d",  date = td)
       Date_Time (2014, 9, 22, 17, 23, 42, 0)

       >>> Date_Time.from_string_x ("15:40", date = td, time = tt)
       Date_Time (2014, 9, 19, 15, 40, 0, 0)

       >>> Date_Time.from_string_x ("15:40", date = td, time = tt, future = True)
       Date_Time (2014, 9, 20, 15, 40, 0, 0)

       >>> Date_Time.from_string_x ("18:40", date = td, time = tt)
       Date_Time (2014, 9, 19, 18, 40, 0, 0)

       >>> Date_Time.from_string_x ("18:40", date = td, time = tt, future = True)
       Date_Time (2014, 9, 19, 18, 40, 0, 0)

       >>> print (Date_Time (2004, 10, 15, 16,  3, 14).yyyy_mm_dd_HH_MM)
       2004-10-15 16:03
       >>> print (Date_Time (2004, 10, 15, 16,  3, 34).yyyy_mm_dd_HH_MM)
       2004-10-15 16:04
    """

    _Type            = datetime.datetime
    _default_format  = "%Y-%m-%d %H:%M:%S"
    _init_arg_names  = \
        CAL.Date._init_arg_names + CAL.Time._init_arg_names
    _kind            = "datetime"
    _timetuple_slice = lambda s, tt : tt [:6] + (0, )

    time_pattern     = Regexp \
        ( r"(?P<hour> \d{2,2})"
          r":"
          r"(?P<minute> \d{2,2})"
          r"(?: :"
            r"(?P<second> \d{2,2})"
            r"(?: \."
              r"(?P<microsecond> \d+)"
            r")?"
          r")?"
          r"(?: \s?"
            r"(?P<tzinfo> [-+]\d{4,4})"
          r")?"
        , flags = re.VERBOSE | re.IGNORECASE
        )

    from _CAL.Delta import Date_Time_Delta as Delta

    @Once_Property
    def dst_adjustment (self) :
        """Daylight saving time (DST) adjustment, as a timedelta object.

        if DST information isn't known, return None.
        """
        result = self._body.dst ()
        if result is not None :
            result = self.Delta (seconds = result.seconds)
        return result
    # end def dst_adjustment

    @Once_Property
    def JT (self) :
        """Time of day based on JD as decimal fraction.

        Julian dates start at noon, therefore a result of `0` means noon, a
        result of `0.5` meeans midnight, and so on.
        """
        JD = self.JD2000
        return JD - int (JD)
    # end def JT

    @Once_Property
    def midnight (self) :
        return self.replace (hour=0, minute=0, second=0, microsecond=0)
    # end def midnight

    @Once_Property
    def noon (self) :
        return self.replace (hour=12, minute=0, second=0, microsecond=0)
    # end def noon

    @Once_Property
    def yyyy_mm_dd_HH_MM (self) :
        "Return formatted date/time value with rounded minutes"
        dt = self + datetime.timedelta (seconds = 30)
        return dt.formatted ("%Y-%m-%d %H:%M")
    # end def yyyy_mm_dd_HH_MM

    def as_date (self) :
        """Return `self` converted to pure `Date`."""
        return CAL.Date (date = self._body.date ())
    # end def as_date

    def as_local (self, tz = None) :
        """Return `self` converted to local time.

        If `astimezone` is called without explicit `tz`, the returned result
        does not have daylight saving time (DST) information. Therefore,
        passing the local `tz` is recommended if `dst_adjustment` is needed.
        """
        return self.__class__ (** {self._kind : self._body.astimezone (tz)})
    # end def as_local

    def as_time (self) :
        """Return `self` converted to pure `Time`."""
        return CAL.Time (time = self._body.time ())
    # end def as_time

    def as_utc (self) :
        """Return `self` converted to `UTC`."""
        local = self.as_local ()
        delta = self.Delta    (seconds = local._body.utcoffset ().seconds)
        return local - delta
    # end def as_utc

    @classmethod
    def combine (cls, date, time) :
        """Create a `Date_Time` object from `date` and `time` objects."""
        if isinstance (date, CAL._DTW_) :
            date = date._body
        if isinstance (time, CAL._DTW_) :
            time = time._body
        return cls (** {cls._kind : datetime.datetime.combine (date, time)})
    # end def combine

    @staticmethod
    def from_ical (ical) :
        for p_cls, tgl_cls in \
            ( (datetime.datetime,   CAL.Date_Time)
            , (datetime.date,       CAL.Date)
            , (datetime.timedelta,  CAL.Time_Delta)
            ) :
            if isinstance (ical.dt, p_cls) :
                return tgl_cls (** {tgl_cls._kind : ical.dt})
    # end def from_ical

    @classmethod
    def from_string (cls, s) :
        return cls.__c_super.from_string (s, check_tail = False)
    # end def from_string

    @classmethod
    def from_string_x (cls, s, ** kw) :
        """Convert `s` to `Date_Time`.

           `s` can be a valid string representation of

           * a date and time value

           * a date and time delta value (relative to `now` at the time of call)

           * a time value (relative to today's date at the time of call)

           Possible keyword arguments are:

           * `future`: if `s` is a time value smaller than `now`, force
             `result` to tomorrow

           * `date`: apply delta or time value `s` to `date` instead of `now`

           * `time`: compare time value `s` to `time` instead of `now`

        """
        v = s.strip ()
        if v.startswith (("+", "-")) :
            return cls._from_string_delta (v, ** kw)
        else :
            try :
                return cls.from_string (v)
            except ValueError :
                return cls._from_string_time (v, ** kw)
    # end def from_string_x

    @classmethod
    def from_julian (cls, jd, kind = "CJD") :
        k = kind
        if kind.endswith ("S") :
            jd /= 86400.0
            k = kind [:-1] + "D"
        days          = int (jd)
        seconds       = (jd - days) * 86400
        result = super (Date_Time, cls).from_julian (days, kind = k)
        return result + CAL.Time_Delta (seconds = seconds)
    # end def from_ordinal

    @classmethod
    def _from_string_delta (cls, s, ** kw) :
        now   = kw.get ("date") or cls ()
        delta = cls.Delta.from_string (s)
        return now + delta
    # end def _from_string_delta

    @classmethod
    def _from_string_match_kw (cls, s, match) :
        assert match
        kw = super (Date_Time, cls)._from_string_match_kw (s, match)
        t  = s [match.end () :].lstrip ().lstrip ("T")
        if t :
            match = cls.time_pattern.match (t)
            if match and match.end () == len (t.rstrip ()) :
                kw.update (CAL.Time._from_string_match_kw (t, match))
            else :
                raise ValueError (s)
        return kw
    # end def _from_string_match_kw

    @classmethod
    def _from_string_time (cls, s, ** kw) :
        future = kw.get ("future")
        date   = kw.get ("date")   or CAL.Date ()
        now    = kw.get ("time")   or CAL.Time ()
        time   = CAL.Time.from_string (s)
        if future and time < now :
            date += 1
        return cls.combine (date, time)
    # end def _from_string_time

    def __getattr__ (self, name) :
        result = self.__super.__getattr__ (name)
        if name in self.JD_offset :
            if name.endswith ("S") :
                result += self.seconds
            else :
                result += (self.seconds / 86400.)
            setattr (self, name, result)
        return result
    # end def __getattr__

# end class Date_Time

class Date_Time_M (CAL._Mutable_DTW_) :
    """Mutable datetime object

       >>> from _TFL.json_dump import to_string as jsonified
       >>> d1 = d2 = Date_Time_M (2004, 10, 15, 16,  3, 14)
       >>> print (d1, d2)
       2004-10-15 16:03:14 2004-10-15 16:03:14
       >>> id (d1) == id (d2)
       True
       >>> d1 += 1
       >>> print (d1, d2)
       2004-10-16 16:03:14 2004-10-16 16:03:14
       >>> id (d1) == id (d2)
       True
       >>> print (jsonified ((d1, d2)))
       ["2004-10-16T16:03:14", "2004-10-16T16:03:14"]

    """

    Class = Date_Time

# end class Date_Time_M

class _Date_Time_Arg_ (TFL.CAO.Opt.Date) :
    """Argument or option with a (calendary) date/time value"""

    _real_name = "Date_Time"

    @Class_and_Instance_Once_Property
    def _CAL_Type (soc) :
        """Import `Date_Time` from `CAL.Date_Time`

        Otherwise, `__main__.Date_Time` vs. `CAL.Date_Time` confusion is
        possible.
        """
        from _CAL.Date_Time import Date_Time
        return Date_Time
    # end def _CAL_Type

# end class _Date_Time_Arg_

def datetime_utcnow () :
    """Return the current UTC date and time, with tzinfo None.

    Drop-in replacement for the `datetime.utcnow` function deprecated by
    Python 3.12.
    """
    return Date_Time ().as_utc ()._body.replace (tzinfo=None)
# end def datetime_utcnow

def _main (cmd) :
    base = cmd.base
    if cmd.offset :
        base  += cmd.offset
    if cmd.relative_delta :
        ### need to do this by hand here to avoid module-level circular import
        import _CAL.Relative_Delta
        delta  = CAL.Relative_Delta.from_string (cmd.relative_delta)
        base  += delta
    if cmd.delta_to :
        print (base - cmd.delta_to)
    else :
        print (base.formatted (cmd.format))
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler     = _main
    , args        =
        ( TFL.CAO.Opt.Date_Time
            ( name          = "base"
            , default       = "now"
            , description   = "Base date_time to operate on"
            )
        ,
        )
    , opts        =
        ( TFL.CAO.Opt.Date_Time
            ( name          = "delta_to"
            , description   = "Print `base - delta_to`"
            )
        , "-format:S=%Y%m%d?Format for date-time (not used for -delta_to)"
        , "-offset:I=0?delta to `base` in days"
        , "-relative_delta:S?Relative delta to `base`"
        )
    , max_args    = 1
    )

if __name__ != "__main__" :
    CAL._Export ("*")
else :
    _Command ()
### __END__ CAL.Date_Time
