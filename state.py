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


class state:

    def __init__(self):
        self.possitions = list()
        self.bar_r = 0
        self.bar_w = 0
        self.over_r = 0
        self.over_w = 0

        for i in range(0, 24):
            self.possitions.append(('n', 0))

        self.possitions[0] = ('r', 2)
        self.possitions[5] = ('w', 5)
        self.possitions[7] = ('w', 3)
        self.possitions[11] = ('r', 5)
        self.possitions[12] = ('w', 5)
        self.possitions[16] = ('r', 3)
        self.possitions[18] = ('r', 5)
        self.possitions[23] = ('w', 2)

        #self.possitions[0] = ('w', 4)
        #self.possitions[3] = ('w', 3)
        #self.possitions[4] = ('w', 3)
        #self.possitions[5] = ('w', 5)
        #self.possitions[20] = ('r', 5)
        #self.possitions[21] = ('r', 3)
        #self.possitions[22] = ('r', 5)
        #self.possitions[23] = ('r', 2)

    def __eq__(self, other):

        if self.bar_r != other.bar_r:
            return False
        if self.bar_w != other.bar_w:
            return False
        for i in range(0, 24):
            if self.possitions[i] != other.possitions[i]:
                return False
        return True

    def __hash__(self):

        p = tuple(self.possitions)
        return hash((self.bar_r, self.bar_w, p))

    def check_home_r(self):
        count = 0
        for i in range(18, 24):
            if self.possitions[i][0] == 'r':
                count = count + self.possitions[i][1]

        return count

    def check_home_w(self):
        count = 0
        for i in range(0, 6):
            if self.possitions[i][0] == 'w':
                count = count + self.possitions[i][1]

        return count

    def normal_move(self, player, pos_old, pos_new):

        pl = self.possitions[pos_new][0]
        if pl == player or pl == 'n':
                p, n = self.possitions[pos_new]
                self.possitions[pos_new] = player, n + 1
                p, n = self.possitions[pos_old]
                if n <= 1:
                    self.possitions[pos_old] = 'n', 0
                else:
                    self.possitions[pos_old] = p, n - 1
                return 1

        elif self.possitions[pos_new][1] == 1:
            p, n = self.possitions[pos_new]
            self.possitions[pos_new] = player, 1
            p, n = self.possitions[pos_old]
            if n <= 1:
                self.possitions[pos_old] = 'n', 0
            else:
                self.possitions[pos_old] = p, n - 1
            if player == 'r':
                self.bar_w = self.bar_w + 1
            else:
                self.bar_r = self.bar_r + 1
            return 1

        else:
            return 0

    def unbar_r(self, number):

        if self.bar_r > 0:
            pos = number - 1
            if self.possitions[pos][0] != 'w':
                self.possitions[pos] = 'r', self.possitions[pos][1] + 1
                self.bar_r = self.bar_r - 1
                return 1
            elif self.possitions[pos][0] == 'w':
                if self.possitions[pos][1] == 1:
                    self.possitions[pos] = 'r', 1
                    self.bar_w = self.bar_w + 1
                    self.bar_r = self.bar_r - 1
                    return 2
                else:
                    return 0
        else:
            return 0

    def unbar_w(self, number):

        if self.bar_w > 0:
            pos = 24 - number
            if self.possitions[pos][0] != 'r':
                self.possitions[pos] = 'w', self.possitions[pos][1] + 1

                self.bar_w = self.bar_w - 1
                return -1
            elif self.possitions[pos][0] == 'r':
                if self.possitions[pos][1] == 1:
                    self.possitions[pos] = 'w', 1
                    self.bar_w = self.bar_w - 1
                    self.bar_r = self.bar_r + 1
                    return 2
                else:
                    return 0
        else:
            return 0

    def check_upper(self, n):
        for i in range(n, 24):
            if self.possitions[i][0] == 'w':
                return True
        return False

    def check_lower(self, n):
        for i in range(0, n, -1):
            if self.possitions[i][0] == 'r':
                return True
        return False

    def count_score_r(self):

        sc = 0
        for i in range(0, 18):
            if self.possitions[i][0] == 'r':
                sc = sc + self.possitions[i][1] * (i + 1)
                if self.possitions[i][1] == 1:
                    if i > 5 and self.check_upper(i):
                        sc = sc - (i + 1) * 20

        for i in range(18, 24):
            if self.possitions[i][0] == 'r':
                sc = sc + self.possitions[i][1] * 20
                if self.possitions[i][1] == 1:
                    sc = sc - (i + 1) * 50

        for i in range(0, 6):
            if self.possitions[i][0] == 'r':
                break
            sc = sc + 20

        sc = sc - self.bar_r * 100
        sc = sc + self.over_r * 600
        return sc

    def count_score_w(self):

        sc = 0
        for i in range(6, 18):
            if self.possitions[i][0] == 'w':
                sc = sc + self.possitions[i][1] * (24 - i)
                if self.possitions[i][1] == 1 and self.check_lower(i):
                    sc = sc - (i + 1) * 20

        for i in range(0, 6):
            if self.possitions[i][0] == 'w':
                sc = sc + self.possitions[i][1] * 20
                if self.possitions[i][1] == 1:
                    sc = sc - (i + 1) * 50

        for i in range(23, 17, -1):
            if self.possitions[i][0] == 'w':
                break
            sc = sc + 20

        sc = sc - self.bar_w * 100
        sc = sc + self.over_w * 600
        return -1 * sc

    def xxx_r(self, pos, number):

        pos_old = pos
        if self.possitions[pos_old][0] != 'r':
            return 0
        if self.possitions[pos_old][1] <= 0:
            return 0
        pos_new = pos + number
        if pos_new > 23:
            return 0
        sc = self.normal_move('r', pos_old, pos_new)
        if sc == 0:
            return 0
        elif sc == 2:
            return 10
        else:
            return 1

    def xxx_w(self, pos, number):

        pos_old = pos
        pos_new = pos - number
        if self.possitions[pos_old][0] != 'w':
            return 0
        if self.possitions[pos_old][1] <= 0:
            return 0
        if pos_new < 0:
            return 0
        sc = self.normal_move('w', pos_old, pos_new)
        if sc == 0:
            return 0
        elif sc == 2:
            return -10
        else:
            return -1
