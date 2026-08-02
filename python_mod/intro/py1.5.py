import datetime
def main():
    
    # a = "seperate"
    # b = "with"
    # c = "sep"

    # print(a, b, c, sep="-")

    # print("Loading", end="")
    # print("... Done!")

    # print(1,2,3,sep=" | ",end="\n\n")

    # def status_line():
    #     print("[STATUS]","System ready.",sep=" ")
    #     print("Time: ", datetime.datetime.now())
    #     print("End of report.")

    # name = input("Enter your name: ")
    # age = int(input("Enter your age: "))
    # age = age + 10
    
    # print(name)
    # print("Your age in 10 years: " + str(age))

    # price = float(input("Enter price: "))
    # print(price)

    # tax = 0.17
    # price = str(f'{(price * (1 + tax)):.3f}')
    # print("Price after tax: " + price)
    # print(f"final price is: {price}")

    # num1 = int(input("number 1: "))
    # num2 = int(input("number 2: "))
    # num3 = int(input("number 3: "))

    # print(f'{((num1 + num2 + num3)/3):.3f}')

    def feet_meters():
        size_feet = float(input("Size in square feet: "))
        convert_ratio = 0.092903
        size_meters = f'{(size_feet * convert_ratio):.4f}'
        print("size in square meters is: " + str(size_meters))


    feet_meters()


if __name__ == "__main__":
    main()