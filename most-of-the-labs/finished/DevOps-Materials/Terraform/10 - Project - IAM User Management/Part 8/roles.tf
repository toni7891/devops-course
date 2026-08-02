locals {
  # Map of role Policies
  role_policies = {
    readonly = [
      "ReadOnlyAccess"
    ]
    admin = [
      "AdministratorAccess"
    ]
    auditor = [
      "SecurityAudit"
    ]
    developer = [
      "AmazonVPCFullAccess",
      "AmazonEC2FullAccess",
      "AmazonRDSFullAccess"
    ]
  }

  role_policies_list = flatten([
    for role, policies in local.role_policies : [
      for policy in policies : {
        role   = role
        policy = policy
      }
    ]
  ])

  # expected output:
  # [
  #   { role = "readonly", policy = "ReadOnlyAccess" },
  #   { role = "admin", policy = "AdministratorAccess" },
  #   { role = "auditor", policy = "SecurityAudit" },
  #   { role = "developer", policy = "AmazonVPCFullAccess" },
  #   { role = "developer", policy = "AmazonEC2FullAccess" },
  #   { role = "developer", policy = "AmazonRDSFullAccess" }
  # ]
}

data "aws_iam_policy" "managed_policies" {
  for_each = toset(local.role_policies_list[*].policy)

  arn = "arn:aws:iam::aws:policy/${each.value}"
}


/*

*/
data "aws_iam_policy_document" "assume_role_policy" {
  for_each = toset(keys(local.role_policies))

  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "AWS"
      identifiers = [
        for user in keys(aws_iam_user.users) : aws_iam_user.users[user].arn
        if contains(local.users_map[user], each.value)
      ]
    }
  }
}

resource "aws_iam_role" "roles" {
  for_each = toset(keys(local.role_policies))

  name               = each.key
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy[each.value].json
}

resource "aws_iam_role_policy_attachment" "role_policy_attachments" {
  count = length(local.role_policies_list) // e.g 6
  role = aws_iam_role.roles[
    local.role_policies_list[count.index].role // e.g. "readonly"
  ].name                                       // e.g. "readonly"
  policy_arn = data.aws_iam_policy.managed_policies[
    local.role_policies_list[count.index].policy // e.g. "ReadOnlyAccess"
  ].arn                                          // arn:aws:iam::aws:policy/ReadOnlyAccess
}

output "data_thing" {
  value = data.aws_iam_policy_document.assume_role_policy
}