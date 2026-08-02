output "commands" {
  description = "Generated SSH commands."
  value       = local.commands
}

output "file_path" {
  description = "Generated SSH commands file path."
  value       = local_file.ssh_commands.filename
}
