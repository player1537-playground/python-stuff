#!/usr/bin/python

# Today's plans:
#   Write your own program
#   Go over functions
#   raw_input and string manipulation

# "abc def ghi"
# ["abc","def","ghi"]

def get_word():
    line = raw_input()
    print "Line: ", line
    words = line.split(' ')
    print "Words: ", words
    word = words[0]
    print "Word: ", word
    return word

x = get_word()
print "The first word you typed was:", x


# Function review

def magic(a, b):
    return a * 2 + b / 3
#          4 * 2 + 5 / 3
  

print magic(4, 5)


def times7(n):
    return n * 7
print times7(5)
