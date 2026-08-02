variable "github_repo" {
  type = string
}

variable "github_repo_suffix" {
  description = "Unique suffix for S3 bucket name (e.g. your username)"
  type        = string
}
