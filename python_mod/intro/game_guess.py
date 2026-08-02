def main():
    yes = ("y","yes")
    no = ("n","no")
    
    want = input("Do you want to play the game? ").lower()
    if want in yes:
        print("Welcome to the guess game!")
        luckyNum = 8
        user_input = int(input("Your guess: "))
        if user_input == luckyNum:
            print("Thats right! You win!")
            print("exiting....")
            
        else:
            print("Thats incorrect!")
            print("Sorry")
            if abs((user_input - luckyNum)) == 1:
                print("Your off by one! try again!")
            
    else:
        print("closing....")
        flag = False
    
if __name__ == "__main__":
    main()