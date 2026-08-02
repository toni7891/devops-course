# Initialize Terraform with the S3 backend configuration
terraform init -backend-config="dev.s3.tfbackend"

# Plan the Terraform configuration to see the changes that will be applied
terraform plan -out dev.plan

# Apply the planned changes to the infrastructure
terraform apply dev.plan 

# To apply new/different backend configuration, use --migrate-state to migrate the existing state to the new backend
terraform init -backend-config="prod.s3.tfbackend" -migrate-state

# To use the regualr in providers.tf file, but chanigng one single value on the s3 backend, you can use -backend-config to override the value in the providers.tf file
terraform init -backend-config="region=eu-west-1" --migrate-state