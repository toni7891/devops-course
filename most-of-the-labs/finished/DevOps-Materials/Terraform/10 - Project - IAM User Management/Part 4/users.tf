locals {
  users_from_yaml = yamldecode(file("${path.module}/user-roles.yaml")).users
}

resource "aws_iam_user" "users" {
  for_each = toset(local.users_from_yaml[*].username)

  name = each.value
}

resource "aws_iam_user_login_profile" "users" {
  for_each        = aws_iam_user.users
  user            = each.value.name
  password_length = 8 // this will generate a random password of length 8 for each user

  // Ignore changes to these attributes to prevent Terraform from trying to update the login profile on every apply
  #? e.g. if the password is changed outside of Terraform, or if the PGP key is updated, 
  #? Terraform will not attempt to reset the password or update the PGP key on the next apply
  lifecycle {
    ignore_changes = [
      password_length,
      password_reset_required,
      pgp_key
    ]
  }
}

output "users" {
  value = local.users_from_yaml
}

output "passwords" {
  sensitive = true
  value = { for user, user_login in aws_iam_user_login_profile.users : user => user_login.password }
}