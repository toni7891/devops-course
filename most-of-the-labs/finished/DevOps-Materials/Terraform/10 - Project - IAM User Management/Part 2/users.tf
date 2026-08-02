locals {
  users_from_yaml = yamldecode(file("${path.module}/user-roles.yaml")).users
}

resource "aws_iam_user" "users" {
  for_each = toset(local.users_from_yaml[*].username)
  
  name = each.value
}

output "users" {
  value = local.users_from_yaml
}
