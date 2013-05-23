#!/usr/bin/python

import math
from proxy import Proxy

class Vector:
    def __init__(self, vector):
        self.vals = vector[:]
    @staticmethod
    def FromN(dimensions, n):
        return Vector([n] * dimensions)
    def __getitem__(self, index):
        return self.vals[index]
    def __len__(self):
        return len(self.vals)
    def __add__(self, other):
        return Vector([self[i] + other[i] for i in xrange(len(self))])
    def __sub__(self, other):
        return self + -other
    def __mul__(self, scalar):
        return Vector([scalar * n for n in self])
    def __neg__(self):
        return self * -1
    def __rmul__(self, scalar):
        return self * scalar
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "[" + ",".join([str(n) for n in self.vals]) + "]"
    def dot(self, other):
        return sum([self[i] * other[i] for i in xrange(len(self))])
    def length(self):
        return math.sqrt(self.dot(self))
    def __pow__(self, n):
        if n == 2:
            return self.dot(self)
    def angle_between(self, other):
        return math.acos(self.dot(other)/(self.length() * other.length()))
    def degrees_between(self, other):
        return math.degrees(self.angle_between(other))
    def cross(self, other):
        assert len(self) == 3
        assert len(other) == 3
        return Vector([self[1] * other[2] - self[2] * other[1],
                       self[2] * other[0] - self[0] * other[2],
                       self[0] * other[1] - self[1] * other[0] ])

class Series(Vector):
    def __init__(self, initial_dict, next_term_fun):
        self.indices = initial_dict
        self.fun = next_term_fun
        self.update_values()
    def update_values(self):
        self.vals = [self.indices[i] for i in sorted(self.indices.keys())]
    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in xrange(index.start, index.stop, index.step)]
        if index in self.indices:
            return self.indices[index]
        val = self.fun(self, index)
        self.indices[index] = val
        self.update_values()
        return val

def continued(p, q, calculate=True):
    # p / q
    r = Series({ 0: p, 1: q}, lambda r, n: r[n-2] % r[n-1])
    a = Series({ }, lambda a, n: r[n-1] // r[n])
    if calculate:
        n = 0
        while r[n] != 0:
            n += 1
        _ = [a[i] for i in xrange(1,n)]
    return a, r

def convergents(a, calculate=True):
    n = len(a)
    P = Series({ 0: 1, -1: 0 }, lambda P, n: a[n]*P[n-1]+P[n-2])
    Q = Series({ 0: 0, -1: 1 }, lambda Q, n: a[n]*Q[n-1]+Q[n-2])
    C = Series({ }, lambda _, n: (0.0 + P[n]) / Q[n])
    if calculate:
        _ = [C[i] for i in xrange(1, n+1)]
    return C, P, Q

def test_continued(p, q):
    p = 0.0 + p
    q = 0.0 + q
    a, r = continued(p, q)
    print "p/q = %s/%s = a = %s\nr=%s" % (p, q, a, r)
    C, P, Q = convergents(a)
    print "C = %s\nP = %s, Q = %s" % (C, P, Q)
    print "C_error = %s" % [C[n] - p/q for n in xrange(1, len(C)+1)]
    print "dC = %s" % [C[n] - C[n-1] for n in xrange(2, len(C)+1)]
    print "(C[n] = %s) = (p/q = %s)" % (C[len(C)], p/q)
    print ""

a, r = continued(Proxy("p"), Proxy("q"), False)
print a[1]
print a[2]
print a[3]
print a[4]
print a[4].value({"p": 121, "q": 21})
C, P, Q = convergents(a, False)
print C[4]
print C[4].value({"p": 1210, "q": 21})
print C[2].value({"p": 314159265, "q": 100000000})
a = Vector([3,1,4,1,5,9,2,6,5])
print convergents(Series({ n:a[n-1] for n in xrange(1,len(a)) }, lambda s,n: s[n]))


def test2():
    #test_continued(Proxy("p"), Proxy("q"))
    #121, 21)
    exit()
    test_continued(51, 31)
    test_continued(354, 100)
    test_continued(233, 177)

def test():
    ahat = Vector([1,2])
    bhat = Vector([3,4])
    print "ahat = %s" % ahat
    print "bhat = %s" % bhat

    print "the sum is %s" % (ahat + bhat)
    c = 3
    print "c = %s" % c
    print "c*ahat = %s" % (c * ahat)
    print "c*bhat = %s" % (c * bhat)
    print "c*bhat + c*hat = %s" % (c * bhat + c * ahat)
    print "c*(bhat+ahat) = %s" % (c * (bhat + ahat))

    print "ahat . ahat = %s" % (ahat.dot(ahat))
    print "ahat ** 2 = %s" % (ahat ** 2)
    print "sqrt(ahat . ahat) = %s" % (math.sqrt(ahat.dot(ahat)))
    print "||ahat|| = %s" % (ahat.length())

    print "ahat . bhat = %s" % (ahat.dot(bhat))
    print "||ahat|| * ||bhat|| = %s" % (ahat.length() * bhat.length())
    print "(ahat.bhat)/(||ahat|| * ||bhat||) = %s" % (ahat.dot(bhat)/(ahat.length() * bhat.length()))
    print "theta = %s" % (ahat.degrees_between(bhat))
    print "phi = %s" % (bhat.degrees_between(ahat))
    chat = Vector([3, 1, 2])
    dhat = Vector([8, 2, 1])
    print "chat = %s, dhat = %s" % (chat, dhat)
    ehat = chat.cross(dhat)
    print "chat x dhat = %s" % (ehat)
    print "ehat . chat = %s" % (ehat.dot(chat))
    print "ehat . dhat = %s" % (ehat.dot(dhat))

    print "-dhat = %s" % (-dhat)
    print "chat - dhat = %s" % (chat - dhat)
