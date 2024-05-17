from xmlrpc.server import SimpleXMLRPCServer
import random


lst1 = [None] * 100
lst2 = [None] * 5

def add(num1,num2):
    return (int(num1)+int(num2))

def sort1(num1,num2,num3,num4,num5):
    x = [num1,num2,num3,num4,num5]
    return sorted(x)

def add_as(num1,num2):
    sum = (int(num1)+int(num2))
    asy = random.randrange(1, 100)
    lst1[asy] = sum
    return asy

def sort_as(num1,num2,num3,num4,num5):
    pointer=0
    x = [num1,num2,num3,num4,num5]
    x = sorted(x)
    lst2.extend(x)
    return ("MESSAGE FROM SERVER: ARRAY RECEIVED")

def ret_arr(val):
    lst3 = lst2[5:10]
    for i in range(0, 5):
        lst2.pop()
    return lst3

def ret(val):
    return lst1[val]

server = SimpleXMLRPCServer(('localhost', 3000), logRequests=True, allow_none=True)
server.register_function(add,"add")
server.register_function(sort1,"sort1")
server.register_function(add_as,"add_as")
server.register_function(ret,"ret")
server.register_function(sort_as,"sort_as")
server.register_function(ret_arr,"ret_arr")
server.serve_forever()