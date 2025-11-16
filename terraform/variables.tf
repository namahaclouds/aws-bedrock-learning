# Variables for AWS Bedrock Learning Project

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1" # Bedrock is available here
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "bedrock-learning"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "bedrock_model_id" {
  description = "Amazon Bedrock model ID to use"
  type        = string
  default     = "anthropic.claude-3-haiku-20240307-v1:0"
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30
}

variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

variable "domain_name" {
  description = "Custom domain name (from GoDaddy)"
  type        = string
  default     = "" # Set this to your domain, e.g., "example.com"
}

variable "github_repo_url" {
  description = "GitHub repository URL for Amplify (optional)"
  type        = string
  default     = ""
}

variable "github_access_token" {
  description = "GitHub personal access token for Amplify (optional)"
  type        = string
  default     = ""
  sensitive   = true
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "BedrockLearning"
    ManagedBy   = "Terraform"
    Environment = "dev"
  }
}
