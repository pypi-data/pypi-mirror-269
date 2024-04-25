# -*- coding: utf-8 -*-
# Copyright (C) 2003-2024 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.Holiday
#
# Purpose
#    Provide information about fixed and moving Austrian holidays
#
# Revision Dates
#    20-Apr-2003 (CT) Creation
#     6-Feb-2004 (CT) Use (y, m, d) tuples instead of strings as dictionary
#                     keys
#     9-Feb-2004 (CT) Dependency on `Y.map` removed
#     5-Jun-2004 (CT) `easter_date` implementation using Spencer Jones'
#                     algorithm added
#    10-Oct-2004 (MG) Use new `CAL.Date_Time` module instead of `Date_Time`
#    15-Oct-2004 (CT) Use `CAL.Date` instead of `CAL.Date_Time`
#    15-Oct-2004 (CT) `_main` and `_command_spec` added
#    17-Oct-2004 (CT) Use `Date_Delta` instead of `Delta`
#    31-Oct-2004 (CT) `_main` changed to display date, too
#     5-Nov-2004 (CT) Use `//` for int division
#    16-Jun-2010 (CT) Use unicode for holiday names
#    16-Jun-2013 (CT) Use `TFL.CAO`, not `TFL.Command_Line`
#    29-Jan-2016 (CT) Modernize, DRY
#     1-Feb-2016 (CT) Add country dependent holidays; remove obsolete code
#     2-Feb-2016 (CT) Factor `CAL.Day_Rule`
#     2-Feb-2016 (CT) Add I18N, german and swiss holidays
#    11-Feb-2016 (CT) Factor `TFL.I18N.test_language`
#    10-May-2020 (CT) Add public holidays of Portugal
#    10-May-2020 (CT) Add doctest for portuguese holidays
#    10-May-2020 (CT) Adapt to change of `CAL.Day_Rule`
#    14-May-2020 (CT) Add `Config` option
#    18-May-2020 (CT) Add `show_by_event`, factor `show_by_year`
#    29-May-2020 (CT) Use `"\v"`, not blank line as separator between events
#    22-Oct-2022 (CT) Call `CAL._Export` unconditionally
#                     * `_main_year` accesses `CAL.holidays` to allow config
#                       files to modify/override the standard holidays
#    27-Feb-2024 (CT) Add `import _CAL.Holiday` to `__main__`
#                     * Remove unconditional `CAL._Export`
#                     * The unconditional `CAL._Export` triggered an exception
#                       due to the export conflicts between `__main__` and
#                       `_CAL` (same name for different objects)
#    ««revision-date»»···
#--

from   _CAL                    import CAL
from   _TFL                    import TFL
from   _TFL.pyk                import pyk

from   _TFL.I18N                import _, _T, _Tn

import _CAL.Date
import _CAL.Day_Rule
import _CAL.Delta

import _TFL.CAO
import _TFL.predicate
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class Holidays (CAL.Day_Rule.Set) :

    F = CAL.Day_Rule.Fixed
    E = CAL.Day_Rule.Easter_Dependent

    ### https://en.wikipedia.org/wiki/List_of_holidays_by_country
    ### https://en.wikipedia.org/wiki/Public_holidays_in_Portugal
    _rules = \
        ( F (_ ("New Year's Day"),                      1,  1)
        , F (_ ("Epiphany"),                            1,  6, "AT")
        , F (_ ("Martin Luther King Day")
             , 1, 1, "US", delta = dict (weekday = F.RD.MO (3))
            )
        , F (_ ("Inauguration Day")
            , 1, 20, "US", y_filter = lambda y : (y % 4 == 1)
            )
        , F (_ ("Washington's Birthday")
            , 2, 1, "US", delta = dict (weekday = F.RD.MO (3))
            )
        , F (_ ("Saint Patrick's Day"),                 3, 17, "IE")
        , F (_ ("Freedom Day"),                         4, 25, "PT")
        , F (_ ("Labor Day"),                           5,  1, "AT", "DE", "PT")
        , F (_ ("May Day Bank Holiday")
            , 5,  1, "UK", delta = dict (weekday = F.RD.MO (1))
            )
        , F (_ ("May Day")
            , 5,  1, "IE"
            , delta = dict (weekday = F.RD.MO (1))
            , y_filter = lambda y : y >= 1994
            )
        , F (_ ("Spring Bank Holiday")
            , 5,  31, "UK", delta = dict (weekday = F.RD.MO (-1))
            )
        , F (_ ("Memorial Day")
            , 5,  31, "US", delta = dict (weekday = F.RD.MO (-1))
            )
        , F (_ ("June Holiday")
            , 6,  1, "IE", delta = dict (weekday = F.RD.MO (1))
            )
        , F (_ ("Portugal Day"),                        6, 10, "PT")
        , F (_ ("Independence Day"),                    7,  4, "US")
        , F (_ ("Swiss National Day"),                  8,  1, "CH")
        , F (_ ("August Holiday")
            , 8,  1, "IE", delta = dict (weekday = F.RD.MO (1))
            )
        , F (_ ("Assumption Day"),                      8, 15, "AT", "PT")
        , F (_ ("Late Summer Bank Holiday")
            , 8,  31, "UK", delta = dict (weekday = F.RD.MO (-1))
            )
        , F (_ ("Labor Day")
            , 9,  1, "US", delta = dict (weekday = F.RD.MO (1))
            )
        , F (_ ("Federal Day of Thanksgiving, Repentance and Prayer")
            , 9, 1, "CH", delta = dict (weekday = F.RD.SU (3))
            )
        , F (_ ("German Unity Day"),                   10,  3, "DE"
            , y_filter = lambda y : y >= 1990
            )
        , F (_ ("Columbus Day")
            , 10,  1, "US", delta = dict (weekday = F.RD.MO (2))
            )
        , F (_ ("Republic Day"),                       10,  5, "PT")
        , F (_ ("Austrian National Day"),              10, 26, "AT")
        , F (_ ("October Holiday")
            , 10,  31, "IE", delta = dict (weekday = F.RD.MO (-1))
            )
        , F (_ ("All Saints' Day"),                    11,  1, "AT", "PT")
        , F (_ ("Veterans Day"),                       11, 11, "US")
        , F (_ ("Thanksgiving")
            , 11,  1, "US", delta = dict (weekday = F.RD.TH (4))
            )
        , F (_ ("Restoration of Independence"),        12,  1, "PT")
        , F (_ ("Feast of the Immaculate Conception"), 12,  8, "AT", "PT")
        , F (_ ("Christmas Day"),                      12, 25, "AT", "CH", "DE", "IE", "PT", "UK", "US")
        , F (_ ("St. Stephen's Day"),                  12, 26, "AT", "CH", "DE", "IE")
        , F (_ ("Boxing Day"),                         12, 26, "UK")
        # easter dependent movable holidays
        , E (_ ("Carnival"),       -47, "PT")
        , E (_ ("Good Friday"),     -2, "CH", "DE", "PT", "UK")
        , E (_ ("Easter Sunday"),    0, "AT", "CH", "DE", "PT", "UK")
        , E (_ ("Easter Monday"),    1, "AT", "CH", "DE", "IE", "UK")
        , E (_ ("Ascension Day"),   39, "AT", "CH", "DE")
        , E (_ ("Whit Sunday"),     49, "AT", "CH", "DE")
        , E (_ ("Whit Monday"),     50, "AT", "CH", "DE")
        , E (_ ("Corpus Christi"),  60, "AT", "PT")
        )

# end class Holidays

holidays = Holidays ()

def _show (year, country, lang = "de") :
    """
    >>> _show (2016, "AT")
      1 2016-01-01 Neujahr
      6 2016-01-06 Hl. Drei Könige
     87 2016-03-27 Ostersonntag
     88 2016-03-28 Ostermontag
    122 2016-05-01 Tag der Arbeit
    126 2016-05-05 Christi Himmelfahrt
    136 2016-05-15 Pfingstsonntag
    137 2016-05-16 Pfingstmontag
    147 2016-05-26 Fronleichnam
    228 2016-08-15 Mariä Himmelfahrt
    300 2016-10-26 Nationalfeiertag
    306 2016-11-01 Allerheiligen
    343 2016-12-08 Mariä Empfängnis
    360 2016-12-25 1. Weihnachtstag
    361 2016-12-26 2. Weihnachtstag

    >>> _show (2016, "DE")
      1 2016-01-01 Neujahr
     85 2016-03-25 Karfreitag
     87 2016-03-27 Ostersonntag
     88 2016-03-28 Ostermontag
    122 2016-05-01 Tag der Arbeit
    126 2016-05-05 Christi Himmelfahrt
    136 2016-05-15 Pfingstsonntag
    137 2016-05-16 Pfingstmontag
    277 2016-10-03 Tag der Deutschen Einheit
    360 2016-12-25 1. Weihnachtstag
    361 2016-12-26 2. Weihnachtstag

    >>> _show (2016, "CH", lang = "en")
      1 2016-01-01 New Year's Day
     85 2016-03-25 Good Friday
     87 2016-03-27 Easter Sunday
     88 2016-03-28 Easter Monday
    126 2016-05-05 Ascension Day
    136 2016-05-15 Whit Sunday
    137 2016-05-16 Whit Monday
    214 2016-08-01 Swiss National Day
    262 2016-09-18 Federal Day of Thanksgiving, Repentance and Prayer
    360 2016-12-25 Christmas Day
    361 2016-12-26 St. Stephen's Day

    >>> _show (2016, "IE")
      1 2016-01-01 Neujahr
     77 2016-03-17 Saint Patrick's Day
     88 2016-03-28 Ostermontag
    123 2016-05-02 Mai-Feiertag
    158 2016-06-06 Juni-Feiertag
    214 2016-08-01 August-Feiertag
    305 2016-10-31 Oktober-Feiertag
    360 2016-12-25 1. Weihnachtstag
    361 2016-12-26 2. Weihnachtstag

    >>> _show (2016, "UK")
      1 2016-01-01 Neujahr
     85 2016-03-25 Karfreitag
     87 2016-03-27 Ostersonntag
     88 2016-03-28 Ostermontag
    123 2016-05-02 Bankfeiertag
    151 2016-05-30 Bankfeiertag
    242 2016-08-29 Bankfeiertag
    360 2016-12-25 1. Weihnachtstag
    361 2016-12-26 2. Weihnachtstag

    >>> _show (2017, "UK", lang = "en")
      1 2017-01-01 New Year's Day
    104 2017-04-14 Good Friday
    106 2017-04-16 Easter Sunday
    107 2017-04-17 Easter Monday
    121 2017-05-01 May Day Bank Holiday
    149 2017-05-29 Spring Bank Holiday
    240 2017-08-28 Late Summer Bank Holiday
    359 2017-12-25 Christmas Day
    360 2017-12-26 Boxing Day

    >>> _show (2016, "US", lang = "en")
      1 2016-01-01 New Year's Day
     18 2016-01-18 Martin Luther King Day
     46 2016-02-15 Washington's Birthday
    151 2016-05-30 Memorial Day
    186 2016-07-04 Independence Day
    249 2016-09-05 Labor Day
    284 2016-10-10 Columbus Day
    316 2016-11-11 Veterans Day
    329 2016-11-24 Thanksgiving
    360 2016-12-25 Christmas Day

    >>> _show (2017, "US", lang = "en")
      1 2017-01-01 New Year's Day
     16 2017-01-16 Martin Luther King Day
     20 2017-01-20 Inauguration Day
     51 2017-02-20 Washington's Birthday
    149 2017-05-29 Memorial Day
    185 2017-07-04 Independence Day
    247 2017-09-04 Labor Day
    282 2017-10-09 Columbus Day
    315 2017-11-11 Veterans Day
    327 2017-11-23 Thanksgiving
    359 2017-12-25 Christmas Day

    >>> _show (2020, "PT", lang = "pt")
      1 2020-01-01 Ano Novo
     56 2020-02-25 Carnaval
    101 2020-04-10 Sexta-feira Santa
    103 2020-04-12 Domingo de Pásco
    116 2020-04-25 Dia da Liberdade
    122 2020-05-01 Dia do Trabalhador
    162 2020-06-10 Dia de Portugal
    163 2020-06-11 Corpus Christi
    228 2020-08-15 Assunção de Nossa Senhora
    279 2020-10-05 Implantação da República
    306 2020-11-01 Dia de Todos-os-Santos
    336 2020-12-01 Restauração da Independência
    343 2020-12-08 Imaculada Conceição
    360 2020-12-25 Natal

    >>> _show (2016, "ANY")
      1 2016-01-01 Neujahr

    """
    show_by_year (holidays, year, country, lang)
# end def _show

_year = CAL.Date ().year

def show_by_event (rule, start, decades, country, language = "de") :
    with TFL.I18N.test_language (language) :
        head = TFL.rounded_down (start, 10)
        tail = head + 10 * decades
        fmt  = "%8s"
        sep  = " ".join (("=" * 4, * (("=" * 8, ) * 10)))
        def _gen_decade (d) :
            for y in range (d, d + 10) :
                evi = rule (y, country)
                yield fmt % ("" if evi is None else evi.event_abbr, )
        print (_T (rule.abbr), getattr (rule, "_start_date", ""))
        print (sep)
        print ("year", * (fmt % ("___" + str (i)) for i in range (10)))
        print (sep)
        for d in range (head, tail, 10) :
            label = ("%4d" % d) [:3] + "_"
            print (label, * _gen_decade (d))
        print (sep)
# end def show_by_event

def _main_event (cmd) :
    ### Use `CAL.holidays`, not `holidays`, to pick up changes from
    ### `Config` file, if any
    rs      = getattr (cmd, "rule_set", CAL.holidays)
    rules   = rs.matching_rules (* cmd.argv)
    country = cmd.country
    for rule in rules :
        if rule.matches (country) :
            show_by_event (rule, cmd.start, cmd.decades, country, cmd.language)
            print ("\v")
# end def _main_event

_Command_Event = TFL.CAO.Cmd \
    ( handler       = _main_event
    , name          = "event"
    , args          =
        ( "rule:S,?Name of rule(s) of events to show"
        ,
        )
    , opts          =
        ( "start:I=%d?First year for which to show events" % (_year - 50, )
        , "decades:I=100?Number of decades for which to show events"
        )
    , min_args      = 1
    )

def show_by_year (rule_set, year, country, language = "de") :
    """Show events in `rule_set` for `year`, `country` and `language`"""
    with TFL.I18N.test_language (language) :
        for _, day in sorted (rule_set (year, country).items ()) :
            date = day.date
            print ("%3d %s %s" % (date.rjd, date, _T (day.description)))
# end def show_by_year

def _main_year (cmd) :
    """Show holidays for `year`, `country` and `language`"""
    ### Use `CAL.holidays`, not `holidays`, to pick up changes from
    ### `Config` file, if any
    rule_set = getattr (cmd, "rule_set", CAL.holidays)
    for year in cmd.argv :
        show_by_year (rule_set, year, cmd.country, cmd.language)
        print ()
# end def _main_year

_Command_Year = TFL.CAO.Cmd \
    ( handler       = _main_year
    , name          = "year"
    , args          =
        ( "year:I,=%d?Year(s) for which to show holidays" % (_year, )
        ,
        )
    , opts          =
        (
        )
    )

_Command = TFL.CAO.Cmd \
    ( args          =
        ( TFL.CAO.Cmd_Choice ("command", _Command_Event, _Command_Year)
        ,
        )
    , opts          =
        ( "-country:S=AT?Country for which to show holidays"
        , "-language:S=de?Language to use for holiday names"
        , TFL.CAO.Opt.Config
            ( "Config"
            , auto_split    = ":"
            , default       = "~/.cal_holiday.config"
            , description   = "File(s) specifying defaults for options"
            , pre_load_cb   = CAL._Import_All
            , x_context     = dict (CAL = CAL)
            )
        ,
        )
    , do_keywords   = True
    , min_args      = 1
    )

if __name__ == "__main__" :
    ### `_main_year` needs to access to features of this module via `CAL`
    ### to allow overriding of `holidays` by config files
    ### --> im, port _CAL.Holiday here
    import _CAL.Holiday
    _Command ()
else :
    CAL._Export ("*")
### __END__ CAL.Holiday
