def main():
    host_port = ("127.0.0.1", 3000)
    print(host_port)
    print(type(host_port))
    print(host_port[0])
    print(host_port[1])
    red_rgb = (255, 0, 0)    
    print(red_rgb[0])
    
    new = (1)
    print(type(new))
    new = (1,)
    print(type(new))
    print(host_port[:1])
    print(host_port[-2:])
    
    service_endpoint = (
        "auth.server.dev.local",
        80
    )
    
    print("domain: " + str(service_endpoint[0]))
    print("port: " + str(service_endpoint[1]))
    
    
if __name__ == "__main__":
    main()