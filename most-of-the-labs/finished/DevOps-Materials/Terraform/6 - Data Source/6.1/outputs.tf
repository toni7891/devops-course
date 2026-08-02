# outputs.tf
output "ubuntu_ami_data_eu" {
  value = data.aws_ami.ubuntu.id
}

# output "ubuntu_ami_data_us" {
#   value = data.aws_ami.ubuntu_us.id
# }