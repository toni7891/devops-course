locals {
  project = "11-multiple-resources"
}

locals {
  ami_ids = {
    ubuntu = data.aws_ami.ubuntu.id
  }
}