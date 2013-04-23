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
import state
import threading


class back:

    def __init__(self):

        self.s = state.state()
        self.mlst = list()
        self.count = 0
        self.lock = threading.Lock()

    def mv_r(self, st, number):
        ls = list()
        for i in range(0, 24):
            tmp = copy.deepcopy(st)
            sc = tmp.xxx_r(i, number)
            if sc != 0:
                ls.append(tmp)
        return ls

    def mv_w(self, st, number):
        ls = list()
        for i in range(0, 24):
            tmp = copy.deepcopy(st)
            sc = tmp.xxx_w(i, number)
            if sc != 0:
                ls.append(tmp)
        return ls

    def move_1_r(self, st, number):

        ls = list()
        tmp = copy.deepcopy(st)
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

    def move_1_w(self, st, number):

        ls = list()
        tmp = copy.deepcopy(st)
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

    def move_2_r(self, st, number):

        ls = list()
        for i in range(18, 24):
            tmp = copy.deepcopy(st)
            pos_old = i
            if tmp.possitions[pos_old][0] != 'r':
                continue
            if tmp.possitions[pos_old][1] <= 0:
                continue
            pos_new = i + number
            if pos_new > 23:
                p, n = tmp.possitions[pos_old]
                if n <= 1:
                    tmp.possitions[pos_old] = 'n', 0
                else:
                    tmp.possitions[pos_old] = p, n - 1
                tmp.over_r = tmp.over_r + 1
            else:
                tmp.normal_move('r', pos_old, pos_new)
            ls.append(tmp)
        return ls

    def move_2_w(self, st, number):

        ls = list()
        for i in range(0, 6):
            tmp = copy.deepcopy(st)
            pos_old = i
            if tmp.possitions[pos_old][0] != 'w':
                continue
            if tmp.possitions[pos_old][1] <= 0:
                continue
            pos_new = i - number
            if pos_new < 0:
                p, n = tmp.possitions[pos_old]
                if n <= 1:
                    tmp.possitions[pos_old] = 'n', 0
                else:
                    tmp.possitions[pos_old] = p, n - 1
                tmp.over_w = tmp.over_w + 1
            else:
                tmp.normal_move('w', pos_old, pos_new)
            ls.append(tmp)
        return ls

    def move(self, st, player, number):
        if player == 'r':
            n = st.check_home_r()
            if n + st.over_r == 15:
                return self.move_2_w(st, number)
            else:
                return self.move_1_w(st, number)
        else:
            n = st.check_home_w()
            if n + st.over_w == 15:
                return self.move_2_r(st, number)
            else:
                return self.move_1_w_r(st, number)

    def double_move(self, st, player, number1, number2):

        ls = self.move(st, player, number1)
        if len(ls) == 0:
            return ls
        lst = list()
        for l in ls:
            lst = lst + self.move(l, player, number2)

        lst2 = list()
        if player == 'r':
            if self.s.bar_r == 0:
                lst2 = self.move(st, player, number1 + number2)
        else:
            if self.s.bar_w == 0:
                lst2 = self.move(st, player, number1 + number2)

        return lst + lst2

    def qd_move(self, st, player, number1, number2):

        br = 0
        moves = 0
        ls = list()
        if player == 'w':
            br = self.s.bar_w
            if br > 0:
                ls = self.move(st, player, number1)
                if len(ls) == 0:
                    return ls
                moves = moves + 1
                if ls[0].bar_w > 0:
                    ls = self.move(ls[0], player, number1)
                    moves = moves + 1
                    if ls[0].bar_w > 0:
                        ls = self.move(ls[0], player, number1)
                        moves = moves + 1
                        if ls[0].bar_w > 0:
                            ls = self.move(ls[0], player, number1)
                            moves = moves + 1
        else:
            br = self.s.bar_r
            if br > 0:
                ls = self.move(st, player, number1)
                if len(ls) == 0:
                    return ls
                moves = moves + 1
                if ls[0].bar_r > 0:
                    ls = self.move(ls[0], player, number1)
                    moves = moves + 1
                    if ls[0].bar_r > 0:
                        ls = self.move(ls[0], player, number1)
                        moves = moves + 1
                        if ls[0].bar_r > 0:
                            ls = self.move(ls[0], player, number1)
                            moves = moves + 1
        if moves == 4:
            return ls

        if len(ls) == 0:
            ls.append(st)

        ls = self.move(ls[0], player, number1)

        if len(ls) == 0:
            return ls

        if moves == 3:
            return ls

        lst = list()
        for l in ls:
            lst = lst + self.move(l, player, number1)
        lst = lst + self.move(ls[0], player, number1 * 2)

        if moves == 2:
            return lst

        lst2 = list()
        for l in lst:
            lst2 = lst2 + self.move(l, player, number1)
        lst2 = lst2 + self.move(ls[0], player, number1 * 3)

        if moves == 1:
            return lst2

        lst3 = list()
        for l in lst2:
            lst3 = lst3 + self.move(l, player, number1)

        lst3 = lst3 + self.move(ls[0], player, number1 * 4)
        lt = self.move(ls[0], player, number1 * 2)
        for l in lt:
            lst3 = lst3 + self.move(l, player, number1 * 2)

        return lst3

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
        self.lock.acquire()
        self.mlst.append((self.expected(lst), st))
        self.count = self.count + 1
        print self.count
        self.lock.release()

    def next_step(self):

        n1, n2 = self.roll_dies()

        print "numbers are ", n1, " & ", n2, "\n"

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

        print "wait !!, em_gammon is thinking..."
        th = list()
        for i in range(0, len(ls)):
            th = threading.Thread(target=self.minimum, args=(ls[i], ))
            th.start()
            print i

        for t in threading.enumerate():
            if t is not threading.currentThread():
                t.join()

        print ""

        self.mlst = sorted(self.mlst)
        if len(self.mlst) > 0:
            self.s = self.mlst[len(self.mlst) - 1][1]
