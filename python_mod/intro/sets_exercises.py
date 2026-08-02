def main():
    ports_list = [8080, 8443, 22, 8080, 443]
    unique_ports = set(ports_list)
    print(type(unique_ports))
    server_names = {"web1", "web2", "web3"}
    if 22 in unique_ports:
        print(True)
    else:
        print(False)
        
    if 22 in server_names:
        print(True)
    else:
        print(False)


    unique_ports.add(3000)
    print(unique_ports)
    
    unique_ports.remove(22)
    print(unique_ports)
    
    unique_ports.add(22)
    print(unique_ports)
    unique_ports.discard(22)
    print(unique_ports)
    
    valid_set = {(1, 2), (3, 4)}
    dupe_set = {1,2,2,4,3,4,6,6}
    dupe_free = set(list(set(dupe_set)))
    print(dupe_free)
    print(type(dupe_free))
    
    
     
if __name__ == "__main__":
    main()