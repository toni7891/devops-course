locals {
  firstnames_from_splat = var.objects_list[*].firstname
}

locals {
  # This will NOT work - Unsupported attribute error
  #! roles_from_splat = local.users_map2[*].roles

  roles_from_splat = [
    for username, user_props in local.users_map2 : user_props.roles
  ]
}

locals {
  roles_from_splat_with_values = values(local.users_map2)[*].roles
}

locals {
  firstnames_from_set = toset(var.objects_list)[*].firstname
}

output "firstnames_from_splat" {
  value = local.firstnames_from_splat
}

output "roles_from_splat" {
  value = local.roles_from_splat
}

output "roles_from_splat_with_values" {
  value = local.roles_from_splat_with_values
}