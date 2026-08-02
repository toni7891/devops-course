

def main(): 
    #     Python = "python"
    # print(Python)

    # profession = "DevOps"
    # print(profession)

    # multi_line = '''Line one 
    # Line two'''
    # print(multi_line)

    # calc = 7/2
    # print("Answer is: " + str(calc))

    # # print(strip("Python for DevOps"))
    
    spaces = "     DevOps     "
    spaces = spaces.strip()
    
    print(spaces)
    print(spaces.upper())
    print(spaces.lower())
    
    path = "/user/local/bin"
    print(path)
    path_list = path.split("/")
    print(path_list)

    new_path_list = "\\".join(path_list)
    print(new_path_list)
    
    path_now = "/user/local/bin"
    new_path_now = path_now + "/python"
    print(new_path_now)
    
    print(new_path_now[3:11])
    
    print(len(new_path_now))
    
    string = "change letter 2"
    new_string = list(string)
    print(new_string)
    new_string[1] = "L"
    finished_string = "".join(new_string)
    print(finished_string)
    # Output -> "cLange letter 2"
    
if __name__ == '__main__':
    main()