def main():
    name = input("State your name: ")
    age = input("State your age: ")
    city = input("State your city: ")
    
    hobbies = input("State 3 hobbies: ")
    hobbies = hobbies.split(" ")
    # print(hobbies[0])
    # print(hobbies[1])
    # print(hobbies[2])
    
    popular_hobbies = ["music", "sports", "gaming", "reading"]
    print(name,age,city,sep=" ")
    
if __name__ == "__main__":
    main()