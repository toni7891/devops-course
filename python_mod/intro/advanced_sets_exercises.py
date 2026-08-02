def main():
    
    set_of_tupels = {(1, 2), (3, 4)}
    print(set_of_tupels)
    
    if (1, 2) in set_of_tupels:
        print(True)
    else:
        print(False)
        
    if (1,3) in set_of_tupels:
        print(True)
    else:
        print(False)
        
        
        
    developers = {"Alice", "Bob", "Charlie"}
    admins = {"Alice", "David"}
    
    Alice_presence = "Alice" in developers | admins
    print(Alice_presence)
    
    Alice_presence = "Alice" in developers.union(admins)
    print(Alice_presence)
    
    Alice_presence = "Alice" in developers.intersection(admins)
    print(Alice_presence)
    
    Alice_presence = "Alice" in developers & admins
    print(Alice_presence)
    
    Alice_presence = "Alice" in developers.difference(admins)
    print(Alice_presence)
    
    Alice_presence = "Alice" in developers - admins
    print(Alice_presence)
    
    developers.intersection_update(admins)
    print(developers)
    
    developers = {"Alice", "Bob", "Charlie"}
    admins = {"Alice", "David"}
    
    developers.intersection(admins)
    print(developers)
    
    
if __name__ == "__main__":
    main()