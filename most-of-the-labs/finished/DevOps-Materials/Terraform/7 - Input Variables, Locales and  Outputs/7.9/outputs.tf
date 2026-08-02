output "s3_bucket_name" {
  value       = aws_s3_bucket.project_bucket.bucket
  description = "The name of the S3 bucket."
}