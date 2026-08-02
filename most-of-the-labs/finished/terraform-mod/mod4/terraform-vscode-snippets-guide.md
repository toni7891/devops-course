# VS Code Custom Snippets for Terraform/AWS

A guide to setting up your own code snippets in VS Code so you can type a short
prefix (like `aws-vpc`) and have it expand into a full, correct Terraform
resource block.

---

## 1. Open the snippet editor

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux).
2. Type **"Snippets: Configure User Snippets"** and select it.
3. Choose **terraform** from the language list.
   - If `terraform` isn't in the list yet, open any `.tf` file first so VS Code
     registers the language, then try again.

This creates (or opens) a file at:

```
~/Library/Application Support/Code/User/snippets/terraform.json      (Mac)
%APPDATA%\Code\User\snippets\terraform.json                          (Windows)
~/.config/Code/User/snippets/terraform.json                          (Linux)
```

## 2. The one rule that trips people up

If you create the file yourself, **the filename must exactly match VS Code's
internal language ID** for it to auto-activate — for `.tf` files that ID is
`terraform`. A file named `tf.json` or `my-snippets.json` will sit there
silently doing nothing, because VS Code doesn't know what language it applies
to.

(Alternative: use **"New Global Snippets file"** instead of picking a
language. That creates a `name.code-snippets` file that works in *all*
languages — but only if you add `"scope": "terraform"` inside each snippet
to restrict it. For Terraform-only snippets, naming the file `terraform.json`
is simpler.)

## 3. Anatomy of a snippet

```jsonc
"Display Name In Suggestion List": {
  "prefix": "trigger-text",
  "body": [
    "line one",
    "line two ${1:placeholder}"
  ],
  "description": "Shown under the suggestion"
}
```

- `prefix` — what you type before pressing `Tab`/`Enter` to expand it.
- `body` — an array of lines (each array entry = one line of inserted code).
- `$1`, `$2`, `$0` — tab stops. Press `Tab` to jump between them in order;
  `$0` is where your cursor ends up last.
- `${1:default text}` — a tab stop pre-filled with text that gets overwritten
  the moment you start typing.
- Reusing the same number (e.g. `${1:bucket}` in three different places)
  keeps all of them in sync — type once, they all update together.

## 4. How to use a snippet

Open any `.tf` file, type the `prefix` (e.g. `aws-sg`), and press `Tab` or
`Enter` when it shows up in the autocomplete popup.

## 5. Install this snippet pack

Paste the JSON below into your `terraform.json` (or merge it into your
existing one), save, then reload VS Code (`Cmd+Shift+P` →
**"Developer: Reload Window"**).

```jsonc
{
	"AWS Provider Boilerplate": {
		"prefix": "aws-provider",
		"body": [
		"terraform {",
		"  required_providers {",
		"    aws = {",
		"      source  = \"hashicorp/aws\"",
		"      version = \"~> ${1:5.0}\"",
		"    }",
		"  }",
		"}",
		"",
		"provider \"aws\" {",
		"  region = \"${2:us-east-1}\"",
		"}"
		],
		"description": "Inserts standard AWS provider configuration block"
	},

	"AWS EC2 Instance": {
		"prefix": "aws-instance",
		"body": [
		"resource \"aws_instance\" \"${1:web}\" {",
		"  ami           = \"${2:ami-0c55b159cbfafe1f0}\"",
		"  instance_type = \"${3:t2.micro}\"",
		"",
		"  tags = {",
		"    Name = \"${4:HelloWorld}\"",
		"  }",
		"}"
		],
		"description": "Inserts a basic standard AWS EC2 resource block"
	},

	"AWS S3 Bucket with Private ACL": {
		"prefix": "aws-s3",
		"body": [
		"resource \"aws_s3_bucket\" \"${1:bucket}\" {",
		"  bucket = \"${2:my-tf-test-bucket}\"",
		"",
		"  tags = {",
		"    Environment = \"${3:Dev}\"",
		"  }",
		"}",
		"",
		"resource \"aws_s3_bucket_ownership_controls\" \"${1:bucket}_oc\" {",
		"  bucket = aws_s3_bucket.${1:bucket}.id",
		"  rule {",
		"    object_ownership = \"BucketOwnerPreferred\"",
		"  }",
		"}",
		"",
		"resource \"aws_s3_bucket_acl\" \"${1:bucket}_acl\" {",
		"  depends_on = [aws_s3_bucket_ownership_controls.${1:bucket}_oc]",
		"",
		"  bucket = aws_s3_bucket.${1:bucket}.id",
		"  acl    = \"private\"",
		"}"
		],
		"description": "Inserts an AWS S3 bucket with ownership controls and private ACL"
	},

	"AWS VPC Boilerplate": {
		"prefix": "aws-vpc",
		"body": [
		"resource \"aws_vpc\" \"${1:main}\" {",
		"  cidr_block       = \"${2:10.0.0.0/16}\"",
		"  instance_tenancy = \"default\"",
		"",
		"  tags = {",
		"    Name = \"${3:main-vpc}\"",
		"  }",
		"}"
		],
		"description": "Inserts a basic Amazon VPC infrastructure resource block"
	},

	"AWS Subnet": {
		"prefix": "aws-subnet",
		"body": [
		"resource \"aws_subnet\" \"${1:public}\" {",
		"  vpc_id            = ${2:aws_vpc.main.id}",
		"  cidr_block        = \"${3:10.0.0.0/24}\"",
		"  availability_zone = \"${4:us-east-1a}\"",
		"",
		"  tags = {",
		"    Name = \"${5:public-subnet}\"",
		"  }",
		"}"
		],
		"description": "Inserts a basic Amazon Subnet resource block"
	},

	"AWS Internet Gateway": {
		"prefix": "aws-igw",
		"body": [
		"resource \"aws_internet_gateway\" \"${1:main}\" {",
		"  vpc_id = ${2:aws_vpc.main.id}",
		"",
		"  tags = {",
		"    Name = \"${3:main-igw}\"",
		"  }",
		"}"
		],
		"description": "Inserts an Internet Gateway attached to a VPC"
	},

	"AWS Route Table (public, IGW route)": {
		"prefix": "aws-route-table",
		"body": [
		"resource \"aws_route_table\" \"${1:public}\" {",
		"  vpc_id = ${2:aws_vpc.main.id}",
		"",
		"  route {",
		"    cidr_block = \"0.0.0.0/0\"",
		"    gateway_id = ${3:aws_internet_gateway.main.id}",
		"  }",
		"",
		"  tags = {",
		"    Name = \"${4:public-rt}\"",
		"  }",
		"}"
		],
		"description": "Inserts a Route Table with a default route to an Internet Gateway (uses block syntax for route, not a map)"
	},

	"AWS Route Table Association": {
		"prefix": "aws-rt-assoc",
		"body": [
		"resource \"aws_route_table_association\" \"${1:public}\" {",
		"  subnet_id      = ${2:aws_subnet.public.id}",
		"  route_table_id = ${3:aws_route_table.public.id}",
		"}"
		],
		"description": "Associates a Subnet with a Route Table"
	},

	"AWS Security Group (SSH + HTTP)": {
		"prefix": "aws-sg",
		"body": [
		"resource \"aws_security_group\" \"${1:web}\" {",
		"  name        = \"${2:web-sg}\"",
		"  description = \"${3:Allow SSH and HTTP inbound}\"",
		"  vpc_id      = ${4:aws_vpc.main.id}",
		"",
		"  ingress {",
		"    description = \"SSH\"",
		"    from_port   = 22",
		"    to_port     = 22",
		"    protocol    = \"tcp\"",
		"    cidr_blocks = [\"0.0.0.0/0\"]",
		"  }",
		"",
		"  ingress {",
		"    description = \"HTTP\"",
		"    from_port   = 80",
		"    to_port     = 80",
		"    protocol    = \"tcp\"",
		"    cidr_blocks = [\"0.0.0.0/0\"]",
		"  }",
		"",
		"  egress {",
		"    from_port   = 0",
		"    to_port     = 0",
		"    protocol    = \"-1\"",
		"    cidr_blocks = [\"0.0.0.0/0\"]",
		"  }",
		"",
		"  tags = {",
		"    Name = \"${5:web-sg}\"",
		"  }",
		"}"
		],
		"description": "Inserts a Security Group allowing inbound SSH/HTTP and all outbound traffic"
	},

	"Terraform Variable Block": {
		"prefix": "tf-variable",
		"body": [
		"variable \"${1:name}\" {",
		"  description = \"${2:description}\"",
		"  type        = ${3:string}",
		"  default     = ${4:null}",
		"}"
		],
		"description": "Inserts a Terraform input variable block"
	},

	"Terraform Output Block": {
		"prefix": "tf-output",
		"body": [
		"output \"${1:name}\" {",
		"  description = \"${2:description}\"",
		"  value       = ${3:resource_reference}",
		"}"
		],
		"description": "Inserts a Terraform output block"
	},

	"AWS Data Source: Latest Amazon Linux AMI": {
		"prefix": "aws-data-ami",
		"body": [
		"data \"aws_ami\" \"${1:amazon_linux}\" {",
		"  most_recent = true",
		"  owners      = [\"amazon\"]",
		"",
		"  filter {",
		"    name   = \"name\"",
		"    values = [\"al2023-ami-*-x86_64\"]",
		"  }",
		"}"
		],
		"description": "Inserts a data source that looks up the latest Amazon Linux AMI"
	}
}
```

## 6. Cheat sheet of prefixes

| Prefix | Inserts |
|---|---|
| `aws-provider` | `terraform { required_providers { aws = ... } }` + `provider "aws"` |
| `aws-vpc` | `aws_vpc` |
| `aws-subnet` | `aws_subnet` |
| `aws-igw` | `aws_internet_gateway` |
| `aws-route-table` | `aws_route_table` with a `0.0.0.0/0` route to an IGW |
| `aws-rt-assoc` | `aws_route_table_association` |
| `aws-sg` | `aws_security_group` (SSH + HTTP ingress, all egress) |
| `aws-instance` | `aws_instance` (EC2) |
| `aws-s3` | `aws_s3_bucket` + ownership controls + private ACL |
| `aws-data-ami` | `data "aws_ami"` (latest Amazon Linux) |
| `tf-variable` | `variable` block |
| `tf-output` | `output` block |

Together these cover a full basic networking stack (VPC → Subnet → Internet
Gateway → Route Table → Association → Security Group) plus the EC2/S3/AMI/
variable/output building blocks you'll need for almost any other lab.

## 7. Common gotcha worth knowing

The AWS provider's `route` argument on `aws_route_table` is a **block**, not
a map — it must be written as:

```hcl
route {
  cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.main.id
}
```

not:

```hcl
route = {
  cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.main.id
}
```

The second form fails `terraform validate` with `Inappropriate value for
attribute "route": set of object required`. The `aws-route-table` snippet
above already uses the correct block syntax.
