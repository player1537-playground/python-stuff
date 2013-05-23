variables = {}
s = ""
while s != "quit":
    s = raw_input()
    inc = None
    if s[-2:] == "++": inc = 1
    if s[-2:] == "--": inc = -1
    if inc != None:
        name = s[0:-2]
        inc = 0
    else:
        name = s
    if name not in variables:
        variables[name] = inc
    else:
        variables[name] = str(int(variables[name]) + inc)
    print name + ": " + str(variables[name])
print variables
