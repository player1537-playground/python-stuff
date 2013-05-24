#!/usr/bin/python

class Oper(object):
    def __init__(self, symbol, fun):
        self.symbol = symbol
        self.fun = fun
    def __call__(self, left, right):
        return self.fun(left, right)
    def __repr__(self):
        return self.symbol
    def __str__(self):
        return self.__repr__()

class OperMaster(object):
    def __init__(self):
        self.opers = { }
    def __add__(self, oper):
        self.opers[str(oper)] = oper
        return self
    def __getitem__(self, symbol):
        return self.opers[symbol]

opers = OperMaster()
opers + \
    Oper("+", lambda a,b: a + b) + \
    Oper("-", lambda a,b: a - b) + \
    Oper("*", lambda a,b: a * b) + \
    Oper("/", lambda a,b: a / b) + \
    Oper("^", lambda a,b: a ** b) + \
    Oper("%", lambda a,b: a % b) + \
    Oper("//", lambda a,b: a // b)


class ProxyNode(object):
    def __init__(self, oper=None, left=None, right=None):
        self.oper = oper
        self.left = left
        self.right = right
    def value(self, mapping):
        # mapping = dict()
        left = self.left
        right = self.right
        if isinstance(left, ProxyNode):
            left = left.value(mapping)
        if isinstance(right, ProxyNode):
            right = right.value(mapping)
        return opers[self.oper](left, right)
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
        if other == 0:
            return self
        return ProxyNode("-", self, other)
    def __rsub__(self, scalar):
        if other == 0:
            return self
        return ProxyNode("-", scalar, self)
    def __mul__(self, other):
        if other == 1:
            return self
        return ProxyNode("*", self, other)
    def __neg__(self):
        return self * -1
    def __div__(self, other):
        if other == 1:
            return self
        return ProxyNode("/", self, other)
    def __rdiv__(self, other):
        return ProxyNode("/", other, self)
    def __rmul__(self, scalar):
        return self * scalar
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        values = (str(self.left), self.oper, str(self.right))
        #print [type(self.left), type(self), type(self.right)]
        if isinstance(self.left, Proxy):
            if isinstance(self.right, Proxy):
                return "%s%s%s" % values
            else:
                if isinstance(self.right, ProxyNode):
                    if self.right.oper == self.oper:
                        return "%s%s%s" % values
                    else:
                        return "%s%s(%s)" % values
                else:
                    return "%s%s%s" % values
        else:
            if isinstance(self.left, ProxyNode) and self.left.oper == self.oper:
                return "%s%s%s" % values
        return "(%s)%s(%s)" % values
    def __rpow__(self, base):
        if other == 1:
            return self
        elif other == -1:
            return 1 / self 
        return ProxyNode("^", base, self)
    def __pow__(self, n):
        return ProxyNode("^", self, n)
    def __mod__(self, other):
        return ProxyNode("%", self, other)
    def __rmod__(self, other):
        return ProxyNode("%", other, self)
    def __floordiv__(self, other):
        return ProxyNode("//", self, other)
    def __rfloordiv__(self, other):
        return ProxyNode("//", other, self)

class Proxy(ProxyNode):
    def __init__(self, initial):
        self.initial = initial
        self.oper = None
    def __repr__(self):
        return str(self.initial)
    def value(self, mapping):
        if self.initial in mapping:
            return mapping[self.initial]
        return self

def test():
    var = "x"
    p = Proxy(var)
    expr = 7 + (p * 3) ** 2 - 1
    print "%s" % (expr)
    mapping = {var: 3}
    print "With (%s), %s = %s" % (mapping, expr, expr.value(mapping))
    print "%s" % ((p+1).value(mapping))

x = Proxy('x')
print x+x
print x+x+x
print x+3+2
print 2+x+3
