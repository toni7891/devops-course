def main():
    
    deployment_targets = [
        "us-east-1",
        "eu-west-1",
        "ap-southeast-1"
        ]

    print(deployment_targets)
    print(deployment_targets[0])
    print(deployment_targets[1])

    deployment_targets.append("us-west-2")
    print(deployment_targets)
    deployment_targets[0] = "us-east-2"

    print(deployment_targets)

    print(len(deployment_targets))

if __name__ == "__main__":
    main()