"""
Author : tharindra galahena (inf0_warri0r)
Project: em_gammon - a backgammon a.i.
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 22/03/2013
License:

     Copyright 2013 Tharindra Galahena

em_gammon is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. em_gammon is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
em_gammon. If not, see http://www.gnu.org/licenses/.

"""

import display
import sys


print ""
print "--------------------------------------------------"
print "       -- EM_GAMMON - A BACKGAMMON A.I. --        "
print "                                                  "
print "   Author : tharindra galahena (inf0_warri0r)     "
print "   Blog   : http://www.inf0warri0r.blogspot.com   "
print "--------------------------------------------------"
print ""

winner = display.display().play()

if winner == 'r':
    print "A.I. wins !!!"
else:
    print "Human wins !!!"

sys.exit()
