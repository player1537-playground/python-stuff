#!/usr/bin/python

Z = range(0,30000)
A_7 = {7*x for x in Z}
A_2 = {2*x for x in Z}
A_total = filter(lambda x: 100 <= x <= 999, A_7.union(A_2))
print sum(A_total)
print A_total[:20]
