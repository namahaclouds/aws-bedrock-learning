# AWS Amplify for Frontend Hosting

# Amplify App
resource "aws_amplify_app" "frontend" {
  name       = "${var.project_name}-frontend"
  repository = var.github_repo_url != "" ? var.github_repo_url : null

  # Build settings for Next.js
  build_spec = <<-EOT
    version: 1
    frontend:
      phases:
        preBuild:
          commands:
            - cd frontend
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: frontend/out
        files:
          - '**/*'
      cache:
        paths:
          - frontend/node_modules/**/*
  EOT

  # Environment variables for the frontend
  environment_variables = {
    NEXT_PUBLIC_API_URL = aws_api_gateway_stage.api_stage.invoke_url
    _LIVE_UPDATES       = "[{\"pkg\":\"next\",\"type\":\"internal\",\"version\":\"latest\"}]"
  }

  # Enable auto branch creation for all branches (optional)
  enable_auto_branch_creation = false
  enable_branch_auto_build    = var.github_repo_url != "" ? true : false
  enable_branch_auto_deletion = false

  # Platform: WEB for SPA/SSG, WEB_COMPUTE for SSR
  platform = "WEB"

  # Custom rules for Next.js routing
  custom_rule {
    source = "/<*>"
    status = "404-200"
    target = "/index.html"
  }

  custom_rule {
    source = "</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|ttf|map|json)$)([^.]+$)/>"
    status = "200"
    target = "/index.html"
  }

  tags = {
    Name = "${var.project_name}-amplify"
  }
}

# Main branch (if using GitHub)
resource "aws_amplify_branch" "main" {
  count       = var.github_repo_url != "" ? 1 : 0
  app_id      = aws_amplify_app.frontend.id
  branch_name = "main"

  enable_auto_build = true

  framework = "Next.js - SSG"
  stage     = "PRODUCTION"

  tags = {
    Name = "${var.project_name}-main-branch"
  }
}

# Domain association (if custom domain is provided)
resource "aws_amplify_domain_association" "custom_domain" {
  count       = var.domain_name != "" ? 1 : 0
  app_id      = aws_amplify_app.frontend.id
  domain_name = var.domain_name

  # Sub domain for main branch
  sub_domain {
    branch_name = var.github_repo_url != "" ? aws_amplify_branch.main[0].branch_name : "main"
    prefix      = ""
  }

  # www subdomain
  sub_domain {
    branch_name = var.github_repo_url != "" ? aws_amplify_branch.main[0].branch_name : "main"
    prefix      = "www"
  }

  wait_for_verification = false
}

# Outputs
output "amplify_app_id" {
  description = "Amplify App ID"
  value       = aws_amplify_app.frontend.id
}

output "amplify_default_domain" {
  description = "Default Amplify domain"
  value       = aws_amplify_app.frontend.default_domain
}

output "amplify_app_url" {
  description = "Amplify app URL"
  value       = "https://${aws_amplify_app.frontend.default_domain}"
}
