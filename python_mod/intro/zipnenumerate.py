def main():
    names = ["Alice", "Bob", "Charlie"]
    servers = ["app-01", "app-02", "app-03"]
    errors = ["disk full", "timeout", "connection lost"]
    ports = [22, 80, 443, 8080]
    
    for name in enumerate(names,start=1):
        print(name)
    
    for index, serv in enumerate(servers,start=1):
        print(index , serv)
        
    for index, error in enumerate(errors):
        if index % 2 == 0:
            print(error)
        
    for index, port in enumerate(ports):
        if index >= 1:
            print(port)
        
    users = ["admin", "dev", "ops"]
    
    for index, name in enumerate(users,start=1):
        print(f"User {index}: {name}")
        
    files = ["log1.txt", "log2.txt", "log3.txt"]
    
    for index, file in enumerate(files):
        if index == (len(files)-1):
            print(file)
            
    regions = ["us-east-1", "eu-west-1", "ap-south-1"]
    for index, region in enumerate(regions):
        if index > 0:
            print(region)
    

    asks = ["backup", "cleanup", "monitoring"]
    for index, ask in enumerate(asks):
        if index % 2 != 0:
            print(ask)

    containers = ["c1", "c2", "c3", "c4"]
    for index, cont in enumerate(containers):
        print(cont)
        if index == 2:
            break
        
    hosts = ["host1", "host2", "host3"]
    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
    
    hosting_pairs = zip(ips, hosts)
        
    for pair in hosting_pairs:
        print(pair)     
                
        
    
if __name__ == "__main__":
    main()