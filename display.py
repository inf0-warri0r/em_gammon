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

import back


class display:

    def __init__(self):
        self.b = back.back()

    def print_bord(self):

        print "------------------", self.b.s.bar_r, "-------------------\n"
        r = ""
        s = ""
        for i in range(12, 24):
            if i == 18:
                s = s + "| | "
                r = r + "| |-"
            r = r + str(i) + "-"
            s = s + str(self.b.s.possitions[i][0]) + "  "

        print r
        print s
        s = ""
        r = ""
        for i in range(12, 24):
            if i == 18:
                s = s + "| | "
                r = r + "| | "
            s = s + str(self.b.s.possitions[i][1]) + "  "
            r = r + "   "

        print s
        print r
        print r
        s = ""
        for i in range(11, -1, -1):
            if i == 5:
                s = s + "| | "
                r = r + "| | "
            s = s + str(self.b.s.possitions[i][0]) + "  "

        print s

        r = ""
        s = ""

        for i in range(11, 9, -1):
            r = r + str(i) + "-"
            s = s + str(self.b.s.possitions[i][1]) + "  "

        for i in range(9, -1, -1):
            if i == 5:
                s = s + "| | "
                r = r + "| |-"
            r = r + str(i) + "--"
            s = s + str(self.b.s.possitions[i][1]) + "  "

        print s
        print r
        print ""
        print "------------------", self.b.s.bar_w, "-------------------\n"

    def empty_bar(self, n1, n2, n3, n4):

        num_of_moves = 0

        if self.b.s.bar_w > 0:
            if n1 == n2:
                pl, num = self.b.s.possitions[24 - n1]
                if pl != 'r' or (pl == 'r' and num == 1):
                    if self.b.s.bar_w > 4:
                        if pl != 'r':
                            self.b.s.possitions[24 - n1] = 'w', num + 4
                        else:
                            self.b.s.possitions[24 - n1] = 'w', 4
                            self.b.s.bar_r = self.b.s.bar_r + 1

                        self.b.s.bar_w = self.b.s.bar_w - 4
                        num_of_moves = num_of_moves + 4
                        n1 = -1
                        n2 = -1
                        n3 = -1
                        n4 = -1
                    else:
                        if pl != 'r':
                            self.b.s.possitions[24 - n1] = 'w', num + self.b.s.bar_w
                        else:
                            self.b.s.possitions[24 - n1] = 'w', self.b.s.bar_w
                            self.b.s.bar_r = self.b.s.bar_r + 1

                        num_of_moves = num_of_moves + self.b.s.bar_w
                        if self.b.s.bar_w == 1:
                            n1 = -1
                        elif self.b.s.bar_w == 2:
                            n1 = n2 = -1
                        elif self.b.s.bar_w == 3:
                            n1 = n2 = n3 = -1
                        self.b.s.bar_w = 0

            else:
                pl1, num1 = self.b.s.possitions[24 - n1]
                pl2, num2 = self.b.s.possitions[24 - n2]

                if pl1 != 'r' or (pl1 == 'r' and num1 == 1):
                    if pl2 != 'r' or (pl2 == 'r' and num2 == 1) and self.b.s.bar_w == 1:

                        p1 = int(raw_input("to : "))
                        while p1 != 24 - n1 and p1 != 24 - n2:
                            print "wrong move\n"
                            p1 = int(raw_input("to : "))

                        l, m = self.b.s.possitions[p1]
                        if l != 'r':
                            self.b.s.possitions[p1] = 'w', m + 1
                        else:
                            self.b.s.possitions[p1] = 'w', 1
                            self.b.s.bar_r = self.b.s.bar_r + 1

                        if p1 == 24 - n1:
                            n1 = -1
                        elif p1 == 24 - n2:
                                n2 = -1
                        self.b.s.bar_w = self.b.s.bar_w - 1
                        num_of_moves = num_of_moves + 1

                    elif pl2 != 'r' or (pl2 == 'r' and num2 == 1):
                        if pl1 != 'r':
                            self.b.s.possitions[24 - n1] = 'w', num1 + 1
                        else:
                            self.b.s.possitions[24 - n1] = 'w', 1
                            self.b.s.bar_r = self.b.s.bar_r + 1

                        if pl2 != 'r':
                            self.b.s.possitions[24 - n2] = 'w', num2 + 1
                        else:
                            self.b.s.possitions[24 - n2] = 'w', 1
                            self.b.s.bar_r = self.b.s.bar_r + 1

                        self.b.s.bar_w = self.b.s.bar_w - 2
                        num_of_moves = num_of_moves + 2
                        n1 = -1
                        n2 = -1
                    else:
                        if pl1 != 'r':
                            self.b.s.possitions[24 - n1] = 'w', num1 + 1
                        else:
                            self.b.s.possitions[24 - n1] = 'w', 1
                            self.b.s.bar_r = self.b.s.bar_r + 1

                        self.b.s.bar_w = self.b.s.bar_w - 1
                        num_of_moves = num_of_moves + 1
                        n1 = -1
                elif pl2 != 'r' or (pl2 == 'r' and num2 == 1):
                    if pl2 != 'r':
                        self.b.s.possitions[24 - n2] = 'w', num2 + 1
                    else:
                        self.b.s.possitions[24 - n2] = 'w', 1
                        self.b.s.bar_r = self.b.s.bar_r + 1

                    self.b.s.bar_w = self.b.s.bar_w - 1
                    num_of_moves = num_of_moves + 1
                    n2 = -1
                else:
                    print "no possible move\n"
                    num_of_moves = -1

        return (num_of_moves, n1, n2, n3, n4)

    def white_move(self, i, n1, n2, n3, n4, num):

        while i < num:

            p1 = int(raw_input("from : "))
            p2 = int(raw_input("to : "))
            home = self.b.s.over_w + self.b.s.check_home_w()
            if p1 > 23:
                print "wrong move\n"
                continue

            p, n = self.b.s.possitions[p1]

            if p != 'w':
                print "wrong move\n"
                continue

            if p2 < 0 and home == 15:

                if n1 != -1 and p1 < n1:
                    n1 = -1
                    i = i + 1
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n2 != -1 and p1 < n2:
                    n2 = -1
                    i = i + 1
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n3 != -1 and p1 < n3:
                    n3 = -1
                    i = i + 1
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n4 != -1 and p1 < n4:
                    n4 = -1
                    i = i + 1
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n1 != -1 and n2 != -1 and p1 < n1 + n2:
                    n1 = -1
                    n2 = -1
                    i = i + 2
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n3 != -1 and n4 != -1 and p1 < n3 + n4:
                    n3 = -1
                    n4 = -1
                    i = i + 2
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n1 != - 1 and n2 != -1 and n3 != -1 and p1 < n1 * 3:
                    n1 = -1
                    n2 = -1
                    n3 = -1

                    i = i + 3
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n2 != - 1 and n3 != -1 and n4 != -1 and p1 < n2 * 3:
                    n2 = -1
                    n3 = -1
                    n4 = -1
                    i = i + 3
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                if n1 != - 1 and n2 != -1 and n3 != -1 and n4 != -1 and p1 < n1 * 4:
                    n1 = -1
                    n2 = -1
                    n3 = -1
                    n4 = -1
                    i = i + 4
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = 'w', n - 1
                    self.b.s.over_w = self.b.s.over_w + 1
                    continue
                print "wrong move 3\n"
                continue

            elif p2 < 0 and home < 15:
                print "wrong move 4\n"
                continue

            q, m = self.b.s.possitions[p2]

            if q == 'r' and m > 1:
                print "wrong move\n"
                continue

            if n1 != -1 and p1 - p2 == n1:
                n1 = -1
                i = i + 1
            elif n2 != -1 and p1 - p2 == n2:
                n2 = -1
                i = i + 1
            elif n3 != -1 and p1 - p2 == n3:
                n3 = -1
                i = i + 1
            elif n4 != -1 and p1 - p2 == n4:
                n4 = -1
                i = i + 1
            elif p1 - p2 == n1 + n2:
                n1 = -1
                n2 = -1
                i = i + 2
            elif p1 - p2 == n3 + n4:
                n3 = -1
                n4 = -1
                i = i + 2
            elif p1 - p2 == n2 * 3:
                if n1 != -1 and n2 != -1 and n3 != -1:
                    n1 = -1
                    n2 = -1
                    n3 = -1
                    i = i + 3
                elif n2 != -1 and n3 != -1 and n4 != -1:
                    n2 = -1
                    n3 = -1
                    n4 = -1
                    i = i + 3

            elif n1 != -1 and n2 != -1 and n3 != -1 and n4 != -1:
                if p2 - p1 == n1 * 4:
                    n1 = -1
                    n2 = -1
                    n3 = -1
                    n4 = -1
                    i = i + 4
                else:
                    print "wrong move\n"
                    continue
            else:
                print "wrong move\n"
                continue

            if q != 'r':
                if n == 1:
                    self.b.s.possitions[p1] = 'n', 0
                    self.b.s.possitions[p2] = 'w', m + 1
                else:
                    self.b.s.possitions[p1] = p, n - 1
                    self.b.s.possitions[p2] = 'w', m + 1

            else:
                if m == 1:
                    self.b.s.possitions[p2] = 'w', 1
                    self.b.s.bar_r = self.b.s.bar_r + 1
                    if n == 1:
                        self.b.s.possitions[p1] = 'n', 0
                    else:
                        self.b.s.possitions[p1] = p, n - 1
                else:
                    print "wrong move\n"

    def play(self):

        while 1:

            self.print_bord()

            if self.b.s.over_w == 15:
                return 'w'
            elif self.b.s.over_r == 15:
                return 'r'

            n1, n2 = self.b.roll_dies()

            print "numbers are ", n1, " & ", n2, "\n"

            n3 = -1
            n4 = -1
            num = 2

            if n1 == n2:
                num = 4
                n3 = n1
                n4 = n1

            nm, n1, n2, n3, n4 = self.empty_bar(n1, n2, n3, n4)

            if nm > 0:
                self.print_bord()

            if nm != -1:
                self.white_move(nm, n1, n2, n3, n4, num)

            self.print_bord()

            self.b.next_step()
