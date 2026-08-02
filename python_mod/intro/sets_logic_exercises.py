def main():
    
    friends = {"Bob", "Rolf", "Anne"}
    abroad = {"Bob", "Anne"}
    
    print("friends: ",friends)
    print("aborad: ", abroad)
    print("who is in fiends but not in abroad: ", friends - abroad)
    print("")
    x = set()
    print(x)
    
    local = {"Rolf"}
    abroad = {"Bob", "Anne"}
    
    fiends = local | abroad
    print(friends)
    
    
    art = {"Bob", "Jen", "Rolf", "Charlie"}
    science = {"Bob", "Jen", "Adam", "Anne"}

    print("Common elements: ", art & science)
    
    print("bob in art? ", "Bob" in art)
    print("Anne in art? " , "Anne" in art)
    
    print("Common elements: ", art & science)
    print("only art: ", art - science )
    
    print("only sci: ", science - art )
    print("all students: " ,art | science)    
    
    
    
if __name__ == "__main__":
    main()