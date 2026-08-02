
def num_tuple(strnum):
    listofnums = tuple(map(int, strnum.split(" ")))
    print("how much nums: " , len(listofnums))
    print("Sum of nums: ", sum(listofnums))
    print("avarage: ", (sum(listofnums) / len(listofnums)))
    print(type(listofnums))
    print(listofnums)

def avarageof(strnum):
    print("avarage: ", (sum(strnum) / len(strnum)))


def minmax(strof):
    list_nums = list(map(int, strof.split(" ")))
    minnum = min(list_nums)
    print("min Num: ", minnum)
    maxnum = max(list_nums)
    print("Max num: ", maxnum)

def onlydiv2(strof):
    list_nums = list(map(int, strof.split(" ")))
    list_nums.sort()
    divby2 = []
    for num in list_nums:
        if num % 2 == 0:
            divby2.append(num)

    print("divideable by 2: ", divby2)

def sortbydiv(num):
    if num % 2 == 0:
        print("even")
    else:
        print("ODD")
    
def above60(strof):
    list_nums = list(map(int, strof.split(" ")))
    list_nums.sort()
    passgrade = []
    for num in list_nums:
        if num > 60:
            passgrade.append(num)
    print(passgrade)

def isempty(listof):
    if listof:
        avarageof(listof)
    else:
        print("NONE")
        return None

def reverseof(listof, flag=False):
    new_list = []
    rev = flag
    if rev == False:
        print(listof)
    elif rev == True:
        new_list = list(reversed(listof))
        print(new_list)

    print(rev)
    print(flag)


def randargs(*args):
    listofargs = []
    even = []
    for i in args:
        listofargs.append(i)
        if i % 2 == 0:
            even.append(i)
            even.sort()
    listofargs.sort()
    print(listofargs[-1])
    print("even: ", even)

def main():
    global rev 
    rev = False
    
    #usrin = input("input numbers: ")
    usrin = "4 1 3 2 50"
    grades = "40 50 60 70 80 90 65 61 59"
    passofgrade = [61, 65, 70, 80, 90]
    empty = []
    rand = 4
    num_tuple(usrin)
    minmax(usrin)
    onlydiv2(usrin)
    sortbydiv(rand)
    above60(grades)
    isempty(passofgrade)
    isempty(empty)
    reverseof(passofgrade)
    reverseof(passofgrade, True)
    reverseof(passofgrade)
    randargs(1,2,3,4)
    randargs(5,6)
    



if __name__ == "__main__":
    main()