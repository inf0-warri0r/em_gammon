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

import copy
import random
import thread
import threading
import time


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
        #self.possitions[4] = ('w', 1)
        self.possitions[5] = ('w', 5)
        self.possitions[7] = ('w', 3)
        self.possitions[11] = ('r', 5)
        self.possitions[12] = ('w', 5)
        self.possitions[16] = ('r', 3)
        self.possitions[18] = ('r', 5)
        #self.possitions[22] = ('w', 1)
        self.possitions[23] = ('w', 2)

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
                #print "unbared ", pos, " ", self.possitions[pos]
                return 1
            elif self.possitions[pos][0] == 'w':
                if self.possitions[pos][1] == 1:
                    #p, n = self.possitions[pos]
                    self.possitions[pos] = 'r', 1
                    self.bar_w = self.bar_w + 1
                    self.bar_r = self.bar_r - 1
                    return 2
                else:
                #print 'wrong move'
                    return 0
        else:
            return 0

    def unbar_w(self, number):

        if self.bar_w > 0:
            pos = 24 - number
            if self.possitions[pos][0] != 'r':
                self.possitions[pos] = 'w', self.possitions[pos][1] + 1

                self.bar_w = self.bar_w - 1
                #print "unbared"
                return -1
            elif self.possitions[pos][0] == 'r':
                if self.possitions[pos][1] == 1:
                    #p, n = self.possitions[pos]
                    self.possitions[pos] = 'w', 1
                    self.bar_w = self.bar_w - 1
                    self.bar_r = self.bar_r + 1
                    return 2
                else:
                    #print 'wrong move'
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
                if self.possitions[i][1] == 1 and i > 5 and self.check_upper(i):
                    sc = sc - (i + 1) * 20

        for i in range(18, 24):
            if self.possitions[i][0] == 'r':
                sc = sc + self.possitions[i][1] * 20
                if self.possitions[i][1] == 1 and (self.check_upper(i) or self.bar_w > 0):
                    sc = sc - (i + 1) * 20

        for i in range(0, 6):
            if self.possitions[i][0] == 'r':
                break
            sc = sc + 20

        sc = sc - self.bar_r * 200
        #sc = sc + self.bar_w * 170
        sc = sc + self.over_r * 400
        return sc

    def count_score_w(self):

        sc = 0
        for i in range(0, 18):
            if self.possitions[i][0] == 'w':
                sc = sc + self.possitions[i][1] * (24 - i)
                if self.possitions[i][1] == 1 and i < 18 and self.check_lower(i):
                    sc = sc - (i + 1) * 20

        for i in range(18, 24):
            if self.possitions[i][0] == 'w':
                sc = sc + self.possitions[i][1] * 20
                if self.possitions[i][1] == 1 and (self.check_lower(i) or self.bar_r > 0):
                    sc = sc - (i + 1) * 20

        for i in range(23, 17, -1):
            if self.possitions[i][0] == 'w':
                break
            sc = sc + 20

        #sc = sc + self.bar_r * 170
        sc = sc - self.bar_w * 200
        sc = sc + self.over_w * 400
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


class back:

    def __init__(self):

        self.s = state()
        self.mlst = list()
        self.count = 0
        self.lock = threading.Lock()

    def check_home(self):
        count = 0
        for i in range(18, 24):
            if self.s.possitions[i][0] == 'r':
                count = count + self.s.possitions[i][1]

        return count

    def move_1(self, st, player, number):

        ls = list()
        tmp = copy.deepcopy(st)
        if player == 'r':
            sc = tmp.unbar_r(number)
            if sc == 0:
                if tmp.bar_r > 0:
                    return ls
                else:
                    for i in range(0, 24):
                        tmp = copy.deepcopy(st)
                        sc = tmp.xxx_r(i, number)

                        if sc != 0:
                            ls.append(tmp)
                    return ls
            else:

                ls.append(tmp)
                return ls
        else:
            sc = tmp.unbar_w(number)
            if sc == 0:
                if tmp.bar_w > 0:
                    return ls
                else:
                    for i in range(0, 24):
                        tmp = copy.deepcopy(st)
                        sc = tmp.xxx_w(i, number)

                        if sc != 0:
                            ls.append(tmp)
                    return ls
            else:
                ls.append(tmp)
                return ls

    def move_2(self, st, player, number):

        ls = list()
        tmp = copy.deepcopy(st)
        if player == 'r':
            for i in range(18, 24):
                tmp = copy.deepcopy(st)
                pos_old = i
                if tmp.possitions[pos_old][0] != 'r':
                    continue
                if tmp.possitions[pos_old][1] <= 0:
                    continue
                pos_new = i + number
                if pos_new > 23:
                    p, n = self.possitions[pos_old]
                    if n <= 1:
                        tmp.possitions[pos_old] = 'n', 0
                    else:
                        tmp.possitions[pos_old] = p, n - 1
                    tmp.over_r = tmp.over_r + 1
                else:
                    tmp.normal_move(player, pos_old, pos_new)
                ls.append(tmp)
        else:
            for i in range(18, 24):
                tmp = copy.deepcopy(st)
                pos_old = i
                if tmp.possitions[pos_old][0] != 'w':
                    continue
                if tmp.possitions[pos_old][1] <= 0:
                    continue
                pos_new = i + number
                if pos_new > 23:
                    p, n = self.possitions[pos_old]
                    if n <= 1:
                        tmp.possitions[pos_old] = 'n', 0
                    else:
                        tmp.possitions[pos_old] = p, n - 1
                    tmp.over_w = tmp.over_wr + 1
                else:
                    tmp.normal_move(player, pos_old, pos_new)
                ls.append(tmp)
        return ls

    def move(self, st, player, number):
        if player == 'r':
            n = self.check_home()
            if n + st.over_r == 15:
                return self.move_2(st, player, number)
            else:
                return self.move_1(st, player, number)
        else:
            return self.move_1(st, player, number)

    def double_move(self, st, player, number1, number2):

        ls = self.move(st, player, number1)
        lst = list()
        for l in ls:
            lst = lst + self.move(l, player, number2)

        lst2 = self.move(st, player, number1 + number2)

        return lst + lst2

    def qd_move(self, st, player, number1, number2):

        ls = self.double_move(st, player, number1, number2)
        ls = list(set(ls))

        lst = list()
        for l in ls:
            lst = lst + self.double_move(l, player, number1, number2)
        return lst

    def roll_dies(self):

        n1 = random.randrange(1, 7)
        n2 = random.randrange(1, 7)
        return n1, n2

    def expected(self, lst):

        v = 0.0
        for l in lst:
            v = v + float(l) / 36.0
        return v

    def maximum(self, st):

        lst = list()
        for i in range(1, 7):
            for j in range(i, 7):
                ls = list()
                if i == j:
                    ls = self.qd_move(st, 'r', i, j)
                else:
                    ls = self.double_move(st, 'r', i, j)

                if len(ls) <= 0:
                    lst.append(0)
                    continue
                ls = list(set(ls))
                sc = list()
                for l in ls:
                    sc.append(l[1].count_score('w') + l[1].count_score('r'))
                sc = sorted(sc)
                lst.append(sc[len(sc) - 1])
        return self.expected(lst)

    def minimum(self, st):

        lst = list()
        for i in range(1, 7):
            for j in range(i, 7):
                ls = list()
                if i == j:
                    ls = self.qd_move(st, 'w', i, j)
                else:
                    ls = self.double_move(st, 'w', i, j)
                if len(ls) <= 0:
                    lst.append(0)
                    continue
                ls = set(ls)
                sc = list()

                for l in ls:
                    ns = l.count_score_w() + l.count_score_r()

                    sc.append(ns)

                sc = sorted(sc)
                lst.append(sc[0])
        #return self.expected(lst)
        self.lock.acquire()
        self.mlst.append((self.expected(lst), st))
        self.count = self.count + 1
        print self.count
        self.lock.release()

    def next_step(self):

        n1, n2 = self.roll_dies()
        print n1, " ", n2
        ls = list()
        if n1 == n2:
            ls = self.qd_move(self.s, 'r', n1, n2)
        else:
            ls = self.double_move(self.s, 'r', n1, n2)

        print "len : ", len(ls)
        ls = list(set(ls))
        print "len : ", len(ls)

        self.mlst = list()
        self.count = 0

        for i in range(0, len(ls)):
            #self.minimum(ls[i])
            #self.mlst.append((sc, ls[i]))
            thread.start_new_thread(self.minimum, (ls[i], ))
            #print i

        while self.count < len(ls):
            time.sleep(0.01)
            #pass
        print ""

        self.mlst = sorted(self.mlst)
        if len(self.mlst) > 0:
            self.s = self.mlst[len(self.mlst) - 1][1]


def print_bord(st):

    print "------------------", st.bar_r, "-------------------\n"
    r = ""
    s = ""
    for i in range(12, 24):
        if i == 18:
            s = s + "| | "
            r = r + "| |-"
        r = r + str(i) + "-"
        s = s + str(st.possitions[i][0]) + "  "

    print r
    print s
    s = ""
    r = ""
    for i in range(12, 24):
        if i == 18:
            s = s + "| | "
            r = r + "| | "
        s = s + str(st.possitions[i][1]) + "  "
        r = r + "   "

    print s
    print r
    print r
    s = ""
    for i in range(11, -1, -1):
        if i == 5:
            s = s + "| | "
            r = r + "| | "
        s = s + str(st.possitions[i][0]) + "  "

    print s

    r = ""
    s = ""

    for i in range(11, 9, -1):
        r = r + str(i) + "-"
        s = s + str(st.possitions[i][1]) + "  "

    for i in range(9, -1, -1):
        if i == 5:
            s = s + "| | "
            r = r + "| |-"
        r = r + str(i) + "--"
        s = s + str(st.possitions[i][1]) + "  "

    print s
    print r
    print ""
    print "------------------", st.bar_w, "-------------------\n"

b = back()

while 1:

    print_bord(b.s)
    n1, n2 = b.roll_dies()
    print n1, " ", n2
    num = 2
    if n1 == n2:
        num = 4

    for i in range(0, num):

        p1 = int(raw_input("from : "))
        p2 = int(raw_input("to : "))

        p, n = b.s.possitions[p1]
        q, m = b.s.possitions[p2]

        if q != 'r':
            if n == 1:
                b.s.possitions[p1] = 'n', 0
                b.s.possitions[p2] = 'w', m + 1
            else:
                b.s.possitions[p1] = p, n - 1
                b.s.possitions[p2] = 'w', m + 1

        else:
            if m == 1:
                b.s.possitions[p2] = 'w', 1
                b.s.bar_r = b.s.bar_r + 1
                if n == 1:
                    b.s.possitions[p1] = 'n', 0
                else:
                    b.s.possitions[p1] = p, n - 1

            else:
                print "wrong move"

        print_bord(b.s)

    b.next_step()

print_bord(b.s)
