# -*- coding: utf-8 -*-
# Copyright (C) 2022 Christian Tanzer All rights reserved
# tanzer@gg32.com.
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.display
#
# Purpose
#    Display pdf and svg files
#
# Revision Dates
#     9-Dec-2022 (CT) Creation
#    19-Dec-2022 (CT) Fix typos
#    ««revision-date»»···
#--

from   _TFL import TFL

from   _TFL import sos

import subprocess
import sys

is_macOS_p = sos.uname ().sysname == "Darwin"

def pdf (target) :
    """Display pdf file `target`."""
    if is_macOS_p :
        display_program = "open"
    else :
        display_program = "atril"
    subprocess.run ([display_program, target])
# end def pdf

def svg (target) :
    """Display svg file `target`."""
    if is_macOS_p :
        subprocess.run (["open", target])
    else :
        import webbrowser
        webbrowser.open_new (target)
# end def svg

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ display
