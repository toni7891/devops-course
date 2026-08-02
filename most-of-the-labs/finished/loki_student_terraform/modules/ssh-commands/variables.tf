variable "instances" {
  type = list(object({
    name       = string
    public_ip  = string
    private_ip = string
  }))
  description = "Instances to include in the SSH commands file."
}

variable "private_key_path" {
  type        = string
  description = "Path to the SSH private key."
}

variable "output_path" {
  type        = string
  description = "Path for the generated SSH commands file."
}
