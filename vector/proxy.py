#!/usr/bin/python

from __future__ import division
from numbers import Number

class Oper(object):
    def __init__(self, symbol, oop, fun):
        self.symbol = symbol
        self.fun = fun
        self.oop = oop
    def __call__(self, left, right):
        return self.fun(left, right)
    def __repr__(self):
        return self.symbol
    def __str__(self):
        return self.__repr__()
    def __cmp__(self, other):
        if self.oop < other.oop:
            return -1
        elif self.oop > other.oop:
            return 1
        else:
            return 0

class OperMaster(object):
    def __init__(self):
        self.opers = { }
    def __add__(self, oper):
        self.opers[str(oper)] = oper
        return self
    def __getitem__(self, symbol):
        return self.opers[symbol]

opers = OperMaster()
# [inv,**] > [*,/,%,//] > [-,+] 
opers + \
    Oper("+", 0, lambda a,b: a + b) + \
    Oper("-", 0, lambda a,b: a - b) + \
    Oper("*", 1, lambda a,b: a * b) + \
    Oper("/", 1, lambda a,b: a / b) + \
    Oper("^", 2, lambda a,b: a ** b) + \
    Oper("%", 1, lambda a,b: a % b) + \
    Oper("//", 1, lambda a,b: a // b)


class ProxyNode(object):
    def __init__(self, oper=None, left=None, right=None, ordered=False):
        self.oper = oper
        self.left = left
        self.right = right
        self.ordered = ordered
    def value(self, mapping):
        # mapping = dict()
        left = self.left
        right = self.right
        if isinstance(left, ProxyNode):
            left = left.value(mapping)
        if isinstance(right, ProxyNode):
            right = right.value(mapping)
        return opers[self.oper](left, right)
    def clean_alot(self, n, debug=False):
        ret = self
        while n > 0:
            ret = ret.clean(debug)
            n -= 1
        return ret
    def clean(self, debug=False):
        left_is_proxynode = isinstance(self.left, ProxyNode)
        right_is_proxynode = isinstance(self.right, ProxyNode)
        if left_is_proxynode:
            self.left = self.left.clean()
        if right_is_proxynode:
            self.right = self.right.clean()
        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return self.value()


        vals = None
        current = self
        totest = [
            (ProxyNode('+', {'x':Number}, {'y':Number}), 
             lambda: vals['x'] + vals['y'],
             "3+2 => 5"),
            (ProxyNode('*', {'x':Number}, ProxyNode('*', {'y':Number}, {'rest':None})),
             lambda: vals['rest'] * (vals['x'] * vals['y']),
             "3*(4*[]) => 14*[]"),
            (ProxyNode('+', {'x':Number}, ProxyNode('+', {'y':Number}, {'rest':None})),
             lambda: vals['rest'] + (vals['x'] + vals['y']),
             "3+(2+[]) => 5+[]"),
            (ProxyNode('*', {'x':Number}, ProxyNode('+', {'y':Number}, {'rest':None})),
             lambda: (vals['x']*vals['y']) + (vals['x']*vals['rest']),
             "3*(2+[]) => 3*2+3*[]"),
            (ProxyNode('*', {'x':Number}, ProxyNode('/', {'rest':None}, {'y':Number})),
             lambda: vals['rest'] if vals['x'] == vals['y'] else vals['rest'] * (vals['x'] / vals['y']),
             "6*([]/2) => 3*[]"),
            (ProxyNode('/', ProxyNode('*', {'x':Number}, {'rest':None}), {'y':Number}),
             lambda: vals['rest'] * (vals['x'] / vals['y']),
             "(6*[])/3) => []*2"),
            (ProxyNode('*', {'x':Number}, ProxyNode('+', {'y':None}, {'z':None})),
             lambda: vals['x']*vals['y']+vals['x']*vals['z'],
             "3*([]+[]) => 3*[] + 3*[]"),
            (ProxyNode('/', ProxyNode('+', {'rest':None}, {'top':Number}), {'bottom':Number}),
             lambda: vals['rest']/vals['bottom'] + vals['top'] / vals['bottom'],
             "([]+15)/5 => []/5+3"),
            (ProxyNode('+', ProxyNode('+', {'restl':None}, {'n':Number}), {'restr':None}),
             lambda: (vals['restl'] + vals['restr']) + vals['n'],
             "([]+3)+[] => ([]+[])+3"),
            #(ProxyNode('+', ProxyNode('+', {'restl':None}, {'n':None}), {'restr':None}),
            # lambda: (vals['restl']+vals['restr']) + vals['n'] if vals['restr'] != vals['n'] else vals[None],
            # "([]+[1])+[] => ([]+[])+[1]"),
            #(ProxyNode('+', ProxyNode('+', {'restl':None}, {'n':None}), {'restr':None}),
            # lambda: vals['restl'] + (vals['restr']+vals['n']) if vals['restr'] == vals['n'] else vals[None],
            # "([]+[1])+[1] => []+([1]+[1])"),
            (ProxyNode('+', {'n':Number}, {'rest':None}),
             lambda: ProxyNode('+', vals['rest'], vals['n']),
             "7+[] => []+7"),
            (ProxyNode('+', ProxyNode('*', {'c1':Number}, {'x1':None}), 
                       ProxyNode('*', {'c2':Number}, {'x2':None})),
             lambda: (vals['c1'] + vals['c2']) * vals['x1'] if vals['x1'] == vals['x2'] else vals[None],
             "3*x+2*x => 5*x"),
            (ProxyNode('+', {'x1':None}, {'x2':None}),
             lambda: 2 * vals['x1'] if str(vals['x1']) == str(vals['x2']) else vals[None],
             "x+x => 2*x"),
            (ProxyNode('+', ProxyNode('*', {'c1':Number}, {'x':None}), {'x2':None}),
             lambda: (vals['c1'] + 1) * vals['x'] if str(vals['x']) == str(vals['x2']) else vals[None],
             "3*x+x => 4*x"),
            ]
        for (pattern,fun, example) in totest:
            hasreplaced, vals = match(current, pattern)
            if hasreplaced:
                if debug: print "Replaced: [%s] using %s" % (example, vals)
                res = fun()
                if hash(res) != hash(self):
                    current = res
                    #return current
                    #return fun().clean().clean()
        if hash(current) != hash(self):
            if debug: print "Different [%s] != [%s]" % (str(current), str(self))
            return current
        return self
    def __hash__(self):
        return (hash(self.left) + hash(self.right)) % hash(self.oper)
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if other == None:
            return False
        return hash(self) == hash(other)
    def __ne__(self, other):
        return not (self == other)
    def __getitem__(self, index):
        return self.vals[index]
    def __len__(self):
        return len(self.vals)
    def __add__(self, other):
        if other == 0:
            return self
        return ProxyNode("+", self, other)
    def __radd__(self, scalar):
        return self + scalar
    def __sub__(self, other):
        return self + -other
    #if other == 0:
    #return self
    #return ProxyNode("-", self, other)
    def __rsub__(self, scalar):
        return scalar + -self
    #if scalar == 0:
    #return -self
    #return ProxyNode("-", scalar, self)
    def __mul__(self, other):
        if other == 1:
            return self
        if other == 0:
            return 0
        return ProxyNode("*", self, other)
    def __neg__(self):
        return self * -1
    def __div__(self, other):
        return self.__truediv__(other)
    def __rdiv__(self, other):
        return self.__rtruediv(other)
    def __truediv__(self, other):
        if other == 1:
            return self
        return ProxyNode("/", self, other, True)
    def __rtruediv__(self, other):
        return ProxyNode("/", other, self, True)
    def __rmul__(self, scalar):
        return self * scalar
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        # 3+2*x**1+7
        # 2*(3-x)
        values = (str(self.left), self.oper, str(self.right))
        #print [type(self.left), type(self), type(self.right)]
        if isinstance(self.left, Proxy):
            if isinstance(self.right, Proxy):
                # x . y
                return "%s%s%s" % values
            else:
                if isinstance(self.right, ProxyNode):
                    # x . (3 + y) or x . 2*y
                    if opers[self.right.oper] >= opers[self.oper]:
                        return "%s%s%s" % values
                    else:
                        return "%s%s(%s)" % values
                else:
                    # x . 1
                    return "%s%s%s" % values
        else:
            if isinstance(self.right, Proxy):
                # 2 . y
                return "%s%s%s" % values
            else:
                if isinstance(self.left, ProxyNode):
                    # (3 + x) . y or 2*x . y
                    if opers[self.left.oper] >= opers[self.oper]:
                        return "%s%s%s" % values
                    else:
                        return "(%s)%s%s" % values
                else:
                    # 2 . 3
                    return "%s%s%s" % values
        return "(%s)%s(%s)" % values
    def __rpow__(self, base):
        if other == 1:
            return self
        elif other == -1:
            return 1 / self 
        return ProxyNode("^", base, self, True)
    def __pow__(self, n):
        return ProxyNode("^", self, n, True)
    def __mod__(self, other):
        return ProxyNode("%", self, other, True)
    def __rmod__(self, other):
        return ProxyNode("%", other, self, True)
    def __floordiv__(self, other):
        return ProxyNode("//", self, other, True)
    def __rfloordiv__(self, other):
        return ProxyNode("//", other, self, True)

class Proxy(ProxyNode):
    def __init__(self, initial):
        self.initial = initial
        self.oper = None
    def __hash__(self):
        return hash(self.initial)
    def __repr__(self):
        return str(self.initial)
    def clean(self):
        return self
    def value(self, mapping):
        if self.initial in mapping:
            return mapping[self.initial]
        return self


def match(tomatch, structure):
    ret = dict()
    didmatch = match_(tomatch, structure, ret)
    return didmatch, ret

def match_(tomatch, structure, retdict):
    varname = None
    if isinstance(structure, dict):
        varname = structure.keys()[0]
        structure = structure.values()[0]
    if structure == None:
        retdict[varname] = tomatch
        return True
    if structure == Number:
        if isinstance(tomatch, Number):
            retdict[varname] = tomatch
            return True
        else:
            return False
    if type(tomatch) != type(structure):
        return False
    if isinstance(tomatch, ProxyNode):
        if tomatch.oper != structure.oper:
            return False
        ret = match_(tomatch.left, structure.left, retdict) and \
            match_(tomatch.right, structure.right, retdict)
        if not tomatch.ordered:
            ret = ret or match_(tomatch.right, structure.left, retdict) and \
                match_(tomatch.left, structure.right, retdict)
        if ret:
            retdict[varname] = tomatch
        return ret
    return True

def test_matcher():
#pattern = ProxyNode('*', Number, ProxyNode('*', Number, None))
    x = Proxy('x')
#inp = (3 * x) * 7
    print match(x+3, None)
    print match(x+3, ProxyNode('+', None, Number))
    print match(x+3, ProxyNode('+', Number, None))
    print type(3)
    n = Number
    print isinstance(3, n)
    print match((3*x)*7, ProxyNode('*', { "x": Number }, ProxyNode('*', { "y": Number}, {"rest": None})))
    print match((3*(x+2*7))*7, ProxyNode('*', { "x": Number }, ProxyNode('*', { "y": Number}, {"rest": None})))
    print match(3+x*2, ProxyNode('+', None, ProxyNode('+', None, None)))
    
def test():
    var = "x"
    p = Proxy(var)
    expr = 7 + (p * 3) ** 2 - 1
    print "%s" % (expr)
    mapping = {var: 3}
    print "With (%s), %s = %s" % (mapping, expr, expr.value(mapping))
    print "%s" % ((p+1).value(mapping))


def test3():
    x = Proxy('x')
    print x+x
    print x+x+x
    print x+3+2
    print 2+x+3
    print x+3
    print ((1)-((((0)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(2)))+(((1)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(1)))/(7)))*(1)))+(((1)-((((0)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(2)))+(((1)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(1)))/(7)))*(7)))/(15))
    print "((1)-((((0)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(2)))+(((1)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(1)))/(7)))*(1)))+(((1)-((((0)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(2)))+(((1)-((((1)-((x)*(7)))+(((0)-((x)*(0)))/(1)))*(1)))/(7)))*(7)))/(15))"
    print opers['+'], opers['*'], opers['+'] < opers['*']
    exp = ((((x*7*-1+1)*2*-1+((x*7*-1+1)*-1+1)/7)*-1+1+(((x*7*-1+1)*2*-1+((x*7*-1+1)*-1+1)/7)*7*-1+1)/15)*-1+107+((((x*7*-1+1)*2*-1+((x*7*-1+1)*-1+1)/7)*-1+1+(((x*7*-1+1)*2*-1+((x*7*-1+1)*-1+1)/7)*7*-1+1)/15)*15*-1+16)/22).clean()
    print exp.clean()
test3()
