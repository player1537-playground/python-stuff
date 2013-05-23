#!/usr/bin/python

import sys
import os
import math

debug = len(sys.argv) > 2

def islambda(v):
    return isinstance(v, type(lambda: None)) and v.__name__ == '<lambda>'

def error(message):
    print message
    sys.exit(1)

def isTrue(value):
    return value != [] and value != False and value != None

globalcontext = [ 
    {'name': '+',
     'value': lambda ls, context: reduce(lambda x, y: x + y, ls) },
    {'name': '-',
     'value': lambda ls, context: reduce(lambda x, y: x - y, ls) },
    {'name': 'display',
     'value': lambda ls, context: map(lambda x: sys.stdout.write(str(evaluate(x, context)) + " "), ls)},
    {'name': 'newline',
     'value': lambda ls, context: sys.stdout.write("\n")},
    {'name': '/',
     'value': lambda ls, context: reduce(lambda x, y: x / y, ls)},
    {'name': '*',
     'value': lambda ls, context: reduce(lambda x, y: x * y, ls)},
    {'name': 'if',
     'value': lambda ls, context: evaluate(ls[1] if isTrue(evaluate(ls[0], context)) else (ls[2] if len(ls) == 2 else []), context)},
    {'name': '=',
     'value': lambda ls, context: reduce(lambda x, y: evaluate(x, context) == evaluate(y, context), ls)}
]

def getvalue(name, context):
    value = None
    for var in context:
        if name == var['name']:
            value = var['value']
            if debug: print value
    if value != None:
        return value
    else:
        if name in [var['name'] for var in globalcontext]:
            return getvalue(name, globalcontext)
        else:
            error("Variable `" + name + "' is not defined")

def evaluate(ls, context):
    if isinstance(ls, float):
        return ls
    if isinstance(ls[0], list):
        answer = False
        for x in ls:
            answer = evaluate(x, context)
        return answer
    if debug: print ls, "                    ", context
    command = ls[0]
    rest = ls[1:]
    if command == 'lambda':
        newreturn = {'body': rest[1:], 'args': []}
        for x in rest[0]:
            newreturn['args'].append({'name': x})
        return newreturn
    elif command == 'let':
        newcontext = context[:]
        for pair in rest[0]:
            context.append({'name': pair[0], 'value': evaluate(pair[1], newcontext)})
        if debug: print rest[1:]
        evaluate(rest[1:], context)
    else:
        for index, x in enumerate(rest):
            if isinstance(x, list):
                evaluate(x, context)
            elif isinstance(x, str):
                ls[index+1] = getvalue(x, context)
                if debug: print ls
        function = getvalue(command, context)
        if islambda(function):
            return function(ls[1:], context)
        else:
            newcontext = context[:]
            for index, num in enumerate(rest):
                newcontext.append({ 'value': num, 'name': function['args'][index]['name'] })
            return evaluate(function['body'], newcontext)

def listify(code):
    ls = []
    innumber = insymbol = False
    number = symbol = ''
    newindex = -1
    for index, c in enumerate(code):
        if index < newindex:
            pass
            #sys.stdout.write(c)
        else:
            if debug: sys.stdout.write(c)
            if c == '(':
                newls, newindex = listify(code[index+1:])
                newindex += index + 1 + 1    # Take into account the: last character, and last )
                ls.append(newls)
            elif c.isdigit():
                if innumber:
                    number += c
                else:
                    innumber = True
                    number = c
            elif c.isspace() or c == ')':
                if innumber:
                    ls.append(float(number))
                if insymbol:
                    ls.append(symbol)
                innumber = insymbol = False
            elif not c.isdigit():
                if insymbol:
                    symbol += c
                else:
                    insymbol = True
                    symbol = c
            if c == ')':
                return ls, index
    return ls, len(code)

def main():
    if len(sys.argv) <= 1 or sys.argv[1] == "-":
        filename = "/dev/stdin"
    else: 
        filename = sys.argv[1]
    f = open(filename, 'r')
    code = "".join(f.readlines()).replace('\t', '').replace('\n', ' ')
    codelist, _ = listify(code)
    if debug: print codelist
    evaluate(codelist, [])

if __name__ == "__main__":
    main()
