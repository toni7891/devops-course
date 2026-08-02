resource "random_id" "bucket_suffix" {
  byte_length = 4
}
resource "aws_s3_bucket" "static_website" {
  bucket = "terraform-course-project-one-${random_id.bucket_suffix.hex}"

}


resource "aws_s3_bucket_public_access_block" "static_website" {
  bucket = aws_s3_bucket.static_website.id

  block_public_acls   = false
  block_public_policy = false
}

resource "aws_s3_bucket_website_configuration" "static_website" {
  bucket = aws_s3_bucket.static_website.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.static_website.id
  key          = "index.html"
  source       = "${path.module}/www/index.html"
  etag         = filemd5("${path.module}/www/index.html")
  content_type = "text/html"
}

resource "aws_s3_bucket_policy" "static_website" {
  bucket = aws_s3_bucket.static_website.id
  depends_on = [ aws_s3_bucket_public_access_block.static_website ]
  # Terraform's "jsonencode" function converts a
  # Terraform expression's result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "public-bucket-policy"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource = "${aws_s3_bucket.static_website.arn}/*"
      }
    ]
  })
}

