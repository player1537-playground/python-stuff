# Functions  
def myrange(n):
    array = []
    i = 0
    while n > 0:
        array.append(i)
        n -= 1
        i += 1
    return array

print myrange(6)
print myrange(-20)

def round_num(n, places):
    place = 1
    for x in range(places):
        place *= 10
    return int(n * place + .5) / float(place)

print round_num(1.55555, 3)

def sum_of_array(array):
    ret_sum = 0
    for i in array:
        ret_sum += i
    return ret_sum

array = [1,2 ,3,5,6]
print "sum of that array is: ", sum_of_array(array)

def square(n):
    return n * n

# area of square = side ^ 2
def area(side):
    return square(side)

def superlamearea(side):
    return side * side

print area(5)  # area of a 5x5 square
print area(2.4) # area of a 2.4x2.4 square




exit

def tip(what):
    print "A " + what + " got tipped over"

# array
stuffIOwn = ["mouse", "house", "Turtle", "cow"]

# If statements
if "cow" in stuffIOwn:
    tip("cow")
