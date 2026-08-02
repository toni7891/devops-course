locals {
  users_from_yaml = yamldecode(file("${path.module}/user-roles.yaml")).users
}

output "users" {
  value = local.users_from_yaml
}