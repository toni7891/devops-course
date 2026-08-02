locals {
  name = "Lirone Fitoussi"
  age  = 26
  my_object = {
    key1 = 10
    key2 = "my_value"
  }
}

output "example1" {
  #   value = upper(local.name)

  value = startswith(lower(local.name), "john")
  # This will return true if the name starts with "johh", otherwise false (case insensitive).  
}

output "example2" {
  #   value = local.age * 2
  #   value = abs(local.age)
  value = pow(-15, 2)
}

output "example3" {
  # value = file("${path.module}/users.yaml")
  # value = yamldecode(file("${path.module}/users.yaml"))
  value = yamldecode(file("${path.module}/users.yaml")).users[*].name
}

output "example4" {
  # value = yamlencode(local.my_object)
  value = jsonencode(local.my_object)
}

# resource "local_file" "output_json" {
#   content  = yamlencode(local.my_object)
#   filename = "${path.module}/output.yaml"
# }