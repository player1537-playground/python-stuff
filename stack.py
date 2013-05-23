#!/usr/bin/python

# Zenith 367

import random
import sys

stack = []
def fadd():
    a = stack.pop()
    b = stack.pop()
    stack.append(a+b)

def fsub():
    a = stack.pop()
    b = stack.pop()
    stack.append(b-a)

def fconsole():
    sys.stdout.write(str(stack.pop()))

def fdup():
    a = stack.pop()
    stack.append(a)
    stack.append(a)

def fprint_stack():
    print stack

def fdef():
    name = stack.pop()
    fun = stack.pop()
    user_defs[name] = fun

def fmul():
    a = stack.pop()
    b = stack.pop()
    stack.append(a*b)

def fdiv():
    a = stack.pop()
    b = stack.pop()
    stack.append(b/a)

def fmap():
    new_ls = []
    ls = stack.pop()
    fun = stack.pop()
    fun.insert(0, 0)
    for x in ls:
        print x, new_ls, fun, ls
        fun[0] = x
        evaluate(fun)
        new_ls.append(stack.pop())
    stack.append(new_ls)

def fat():
    index = stack.pop()
    stack.append(stack[-1][index])

def fuck():
    ls = stack.pop()
    evaluate(ls)

def fpop():
    stack.pop()

def fswap():
    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)

def ffor():
    fun = stack.pop()
    step = stack.pop()
    end = stack.pop()
    start = stack.pop()
    x = start
    if debug:
        print start, end, step, fun, stack
    while x <= end:
        if debug:
            print 'in FOR loop, x is: >>', x
            print stack
        stack.append(x)
        evaluate(fun)
        x = stack.pop()
        x += step
        if debug:
            print 'in FOR loop, newx is: >>', x

def flen():
    a = stack.pop()
    stack.append(len(a))

def fset():
    val = stack.pop()
    index = stack.pop()
    stack[-1][index] = val

def fspace():
    stack.append(' ')

def fmake():
    stack.append(' '.join(stack.pop()))

def fsplit():
    separator = stack.pop()
    string = stack.pop()
    stack.append(string.split(separator))

def frandom_min_max():
    mini = stack.pop()
    maxi = stack.pop()
    stack.append(int((maxi-mini) * random.random() + mini))

def frandom():
    stack.append(random.random())

def fequals():
    stack.append(stack.pop() == stack.pop())

def fnot():
    stack.append(not stack.pop())

def fgreater_than():
    stack.append(stack.pop() < stack.pop())

def fless_than():
    stack.append(stack.pop() > stack.pop())

def fgreater_than_or_equals():
    stack.append(stack.pop() <= stack.pop())

def fless_than_or_equals():
    stack.append(stack.pop() >= stack.pop())

def flogical_and():
    stack.append(stack.pop() and stack.pop())

def flogical_or():
    stack.append(stack.pop() or stack.pop())

def fifte():
    els  = stack.pop()
    then = stack.pop()
    cond = stack.pop()
    evaluate(cond)
    if stack.pop() != 0:
        evaluate(then)
    else:
        evaluate(els)

def fpop():
    stack.pop()

def flist_swap():
    i1 = stack.pop()
    i2 = stack.pop()
    print 'flist_swap:', i1, i2, stack
    tmp = stack[-1][i1]
    stack[-1][i1] = stack[-1][i2]
    stack[-1][i2] = tmp

def fstring_to_list():
    string = stack.pop()
    stack.append([x for x in string])

def ffor_each():
    fun = stack.pop()
    ls = stack.pop()
    for x in ls:
        stack.append(x)
        evaluate(fun)

def fclear_stack():
    global stack
    stack = []

def frange():
    stack.append(range(stack.pop()))

def finput():
    print 'rawr'

def fmod():
    a = stack.pop()
    b = stack.pop()
    stack.append(b % a)

def fnewline():
    print

operators = {'+': fadd,
             '-' : fsub,
             'console': fconsole,
             'dup': fdup,
             'print-stack': fprint_stack,
             'def': fdef,
             '*': fmul,
             '/': fdiv,
             'map': fmap,
             'concat': fadd,
             'lat':  fat,
             'swap': fswap,
             'uck': fuck,
             'for': ffor,
             'len': flen,
             'lset': fset,
             'sspace': fspace,
             'smake': fmake,
             'ssplit': fsplit,
             'random-min-max': frandom_min_max,
             'random': frandom,
             '=': fequals,
             'not': fnot,
             '>': fgreater_than,
             '<': fless_than,
             '>=': fgreater_than_or_equals,
             '<=': fless_than_or_equals,
             'and': flogical_and,
             'or': flogical_or,
             'ifte': fifte,
             'pop': fpop,
             'lswap': flist_swap,
             'string-to-list': fstring_to_list,
             'for-each': ffor_each,
             'clear-stack': fclear_stack,
             'range': frange,
             'input': finput,
             '%': fmod,
             'newline': fnewline}

user_defs = {}

inquote = 0
incomment = 0
debug = False

def fun(word):
    if word in [x for x in operators]:
        operators[word]()
    elif word in [x for x in user_defs]:
        evaluate(user_defs[word])
    else:
        print "ERROR: <", word, '>... ', stack, '... ', user_defs, '... ', inquote

def evaluate(ls):
    global inquote
    global list_stack
    global incomment
    for word in ls:
        word = str(word)
        if word == '': continue
        if debug:
            print 'I got: >' + '>' * (inquote+incomment), word, '\t\t\tThe stack is: >>', stack
        if word == '<<)':
            incomment -= 1
        elif incomment > 0:
            continue
        elif word[0] in "1234567890":
            if inquote > 0:
                list_stack.append(int(word))
            else:
                stack.append(int(word))
        elif word[0] == '/' and word != '/':
            if inquote > 0:
                list_stack.append(word)
            else:
                stack.append(word[1:])
        elif word == '(>>':
            incomment += 1
        elif word == '[':
            if inquote == 0:
                list_stack = []
            else:
                list_stack.append('[')
            inquote += 1
        elif word == ']':
            inquote -= 1
            if inquote == 0:
                stack.append(list_stack)
            else:
                list_stack.append(']')
        else:
            if inquote > 0:
                if word[0] == ',' and inquote == 1:
                    fun(word[1:])
                else:
                    list_stack.append(word)
            else:
                fun(word)



if len(sys.argv) > 1: debug = True
while True:
    try:
        line = raw_input()
        evaluate(line.split(' '))
    except EOFError:
        sys.exit(0)
