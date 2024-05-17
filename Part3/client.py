from xmlrpc.client import ServerProxy
import argparse

proxy = ServerProxy('http://localhost:3000', verbose=False)

def add(args):
    num1 = args.add[0]
    num2 = args.add[1]
    sum = proxy.add(num1, num2)
    print("THE SUM OF "+ str(num1) + " AND  " + str(num2) + "RETURNED FROM THE SERVER SYNCHRONOUSLY IS " + str(sum))

def sort1(args):
    num1 = args.sort[0]
    num2 = args.sort[1]
    num3 = args.sort[2]
    num4 = args.sort[3]
    num5 = args.sort[4]
    sorted_list = proxy.sort1(num1,num2,num3,num4,num5)
    print("SORTED ARRAY RETURNED FROM THE SEREVER SYNCHRNOUSLY "+str(sorted_list))

def add_as(args):
    num1 = args.addas[0]
    num2 = args.addas[1]
    print("REQUEST SENT FROM THE SERVER WITH ID "+ str(proxy.add_as(num1, num2)))

def ret(args):
    num1 = args.query[0]
    val = proxy.ret(num1)
    print("SUM RETURNED FROM THE SERVER ASYNHRONOUSLY "+ str(val))

def sort_as(args):
    num1 = args.sort_arr[0]
    num2 = args.sort_arr[1]
    num3 = args.sort_arr[2]
    num4 = args.sort_arr[3]
    num5 = args.sort_arr[4]
    print(str(proxy.sort_as(num1,num2,num3,num4,num5)))

def ret_arr(args):
    num1 = args.query1[0]
    val = proxy.ret_arr(num1)
    print("SORTED ARRAY RETURNED FROM SERVER ASYNCHRONOUSLY "+ str(val))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--add", type=str, nargs=2, metavar=('num1', 'num2'))
    parser.add_argument("-k", "--sort", type=int, nargs=5, metavar=('num1','num2','num3','num4','num5'))
    parser.add_argument("-as", "--addas", type=str, nargs=2, metavar=('num1', 'num2'))
    parser.add_argument("-q", "--query", type=int, nargs=1, metavar=('num1'))
    parser.add_argument("-ks", "--sort_arr", type=int, nargs=5, metavar=('num1','num2','num3','num4','num5'))
    parser.add_argument("-q1", "--query1", type=int, nargs=1, metavar=('num1'))

    args = parser.parse_args()

    if args.add is not None:
        add(args)
    if args.sort is not None:
        sort1(args)
    if args.addas is not None:
        add_as(args)
    if args.query is not None:
        ret(args)
    if args.sort_arr is not None:
        sort_as(args)
    if args.query1 is not None:
        ret_arr(args)
    