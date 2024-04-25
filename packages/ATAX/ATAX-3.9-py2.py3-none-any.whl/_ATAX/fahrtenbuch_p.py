# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package ATAX.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    ATAX.fahrtenbuch_p
#
# Purpose
#    Fahrtenbuch für Fahrten mit Privatfahrzeug (km-Geld)
#
# Revision Dates
#     2-Oct-2017 (CT) Creation
#     1-Jan-2018 (CT) Add `\CR` to `tex_total`, improve `tex_format`
#    ««revision-date»»···
#--

from   _ATAX                    import ATAX
from   _CAL                     import CAL
from   _TFL                     import TFL

from   _ATAX.fahrtenbuch        import FB_Entry, Fahrtenbuch

from   _TFL.EU_Currency         import EUR
from   _TFL.pyk                 import pyk
from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object
import _TFL.CAO

class FB_Entry_P (FB_Entry) :
    """One entry of Fahrtenbuch_P"""

    str_format  = r"  %-11s & %8d & %8d & %-10s & %s"
    tex_format  = r"  %-10s & %6s & %6s & %4d & \tt %s & \sf %s"

    def __init__ (self, date, km_start, km_finis, car, desc, ** kwds) :
        self.car = car
        self.__super.__init__ (date, km_start, km_finis, 0, desc, ** kwds)
    # end def __init__

    @classmethod
    def from_line (cls, line, last) :
        try :
            d, km_start, km_finis, car, desc = \
                [f.strip () for f in line.split ("&", 5)]
        except ValueError :
            raise ValueError ("Split error `%s`" % line)
        else :
            return cls._new_entry (last, d, km_start, km_finis, car, desc)
    # end def from_line

    @classmethod
    def _new_entry (cls, last, d, km_start, km_finis, car, desc) :
        return cls \
            (CAL.Date_Time.from_string (d), km_start, km_finis, car, desc)
    # end def _new_entry

    def tex (self) :
        date    = self.date_formatted
        bus_km  = self.km_business
        desc    = self.desc ### TeX-quote `desc`
        kms     = "%6d" % self.km_start
        kmf     = "%6d" % self.km_finis
        return self.tex_format % (date, kms, kmf, bus_km, self.car, desc)
    # end def tex

    def __str__ (self) :
        date = self.date_formatted
        return self.str_format % \
            (date, self.km_start, self.km_finis, self.car, self.desc)
    # end def __str__

# end class FB_Entry_P

class Fahrtenbuch_P (Fahrtenbuch) :
    """Fahrtenbuch für Fahrten mit Privatfahrzeug (km-Geld)"""

    Entry          = FB_Entry_P
    km_geld        = None

    def tex_total (self, head, tail) :
        kmb  = self.km_business
        kmg  = self.km_geld
        eur  = "\CR" if kmg is None else \
            ("\hfill KM-Geld = %s \CR" % (EUR (kmb * kmg), ))
        return FB_Entry_P.tex_format % ("Total", "", "", kmb, "", eur)
    # end def tex_total

# end class Fahrtenbuch_P

def _main (cmd) :
    ATAX.Command.load_config (cmd)
    Fahrtenbuch_P.km_geld = cmd.km_geld
    fb = Fahrtenbuch_P.from_file (cmd.user, cmd.fahrtenbuch)
    print (fb.tex ())
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler     = _main
    , args        =
        ("fahrtenbuch:P?File defining fahrtenbuch", )
    , min_args    = 1
    , max_args    = 1
    , opts        =
        ( "-Config:P,?Config file(s)"
        , "-user:S=%s" % TFL.Environment.username.capitalize ()
        , "-km_geld:F=0.42"
        , TFL.CAO.Opt.Output_Encoding (default = "iso-8859-15")
        )
    )

if __name__ != "__main__" :
    ATAX._Export ("*")
if __name__ == "__main__" :
    _Command ()
### __END__ ATAX.fahrtenbuch_p
