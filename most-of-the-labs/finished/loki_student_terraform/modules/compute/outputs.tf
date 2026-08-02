output "instances" {
  description = "Instance names, roles, public IPs, and private IPs."
  value = concat(
    [
      {
        name       = aws_instance.loki.tags.Name
        role       = aws_instance.loki.tags.Role
        public_ip  = aws_instance.loki.public_ip
        private_ip = aws_instance.loki.private_ip
      }
    ],
    [
      for instance in aws_instance.nodes : {
        name       = instance.tags.Name
        role       = instance.tags.Role
        public_ip  = instance.public_ip
        private_ip = instance.private_ip
      }
    ]
  )
}
