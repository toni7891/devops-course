# Steps for Implementation

1. Deploy a VPC and a subnet
2. Deploy an Internet Gateway and associate it with the VPC
3. Set up a route table with a route to the Internet Gateway
4. Deploy an EC2 instance inside of the created subnet
5. Associate a public IP and a security group that allows public ingress
6. Replace the original instance with an NGINX Bitnami instance
7. Test access to the website
8. Destroy all resources at the end