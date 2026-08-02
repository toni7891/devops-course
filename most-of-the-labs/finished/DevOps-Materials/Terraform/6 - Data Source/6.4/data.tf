# data "aws_caller_identity" "current" {}

# data "aws_region" "current" {}

# data "aws_region" "us_east" {
#   provider = aws.us_east
# }


# data "aws_vpc" "prod_vpc" {
#   tags = {
#     Env = "NonExistent"
#   }
# }

data "aws_availability_zones" "available" {
  state = "available"
}
