def main():
    
    required_packages = {"python3", "pip", "requests", "boto3", "pip"}

    print(required_packages)
    print("is request inside packages?: " , "requests" in required_packages)    
    print("is ansible inside packages?: " , "ansible" in required_packages) 
    required_packages.add("paramiko")
    required_packages.discard("pip")
    print(required_packages)
    
    installed_packages = {"docker", "python3", "pip"}
    missing = required_packages - installed_packages
    print("missing: ", missing)   
    extra_packages = installed_packages - required_packages
    common_packages = required_packages & installed_packages
    print("extra: ", extra_packages)
    print("common: ", common_packages)
    
    
    
if __name__ == "__main__":
    main()