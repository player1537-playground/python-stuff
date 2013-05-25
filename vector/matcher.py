#!/usr/bin/python

from proxy import Proxy, ProxyNode
from numbers import Number

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
