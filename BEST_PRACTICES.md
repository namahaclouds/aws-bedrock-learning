# AWS Project Best Practices

This document outlines best practices for developing and maintaining this AWS Bedrock project.

## 1. Security Best Practices

### Never Commit Secrets

```bash
# Files that should NEVER be committed:
# - .env, .env.local (contain API keys)
# - terraform.tfvars (may contain secrets)
# - terraform.tfstate (contains sensitive data)
# - AWS credentials files

# These are already in .gitignore - don't remove them!
```

### Use IAM Roles, Not Access Keys

- Lambda uses IAM roles (not hardcoded credentials)
- Never put AWS access keys in code
- Use `aws configure` for local development only
- For production, use IAM roles for EC2/ECS or OIDC for GitHub Actions

### Principle of Least Privilege

```hcl
# In terraform/iam.tf, Lambda only has:
# - bedrock:InvokeModel (not bedrock:*)
# - CloudWatch Logs write permissions
# - No other AWS service access

# When adding permissions, only add what's needed
```

### Enable CloudWatch Logging

All Lambda invocations are logged for debugging and security auditing.

```bash
# View logs
aws logs tail /aws/lambda/bedrock-learning-query-function --follow
```

## 2. Cost Optimization

### Use Appropriate Bedrock Models

```
Claude 3 Haiku:   $0.00025/1K input tokens  (learning/testing)
Claude 3 Sonnet:  $0.003/1K input tokens    (production)
Claude 3 Opus:    $0.015/1K input tokens    (when needed)
```

Start with Haiku for development.

### Set Up Billing Alerts

1. AWS Console → Billing → Budgets
2. Create monthly budget
3. Set alert at $10, $25, $50

### Monitor Costs

```bash
# Check current month costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Implement Rate Limiting

Add rate limiting in API Gateway:
- Usage plans
- API keys
- Throttling settings

### Cleanup Unused Resources

```bash
# List all Lambda functions
aws lambda list-functions

# Delete old versions
aws lambda delete-function --function-name old-function-name

# Destroy test infrastructure
cd terraform
terraform destroy
```

## 3. Development Workflow

### Use Git Branching Strategy

```bash
# Main branch for production
git checkout main

# Feature branches for development
git checkout -b feature/add-streaming

# Don't commit directly to main
```

### Test Locally Before Deploying

```bash
# Test Lambda locally
cd lambda
source ../venv/bin/activate
python handler.py

# Test frontend locally
cd frontend
npm run dev

# Only deploy after local testing passes
```

### Use Terraform Workspaces for Environments

```bash
# Create workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch between environments
terraform workspace select dev
terraform apply
```

### Keep Dependencies Updated

```bash
# Python dependencies
cd lambda
pip list --outdated

# Node dependencies
cd frontend
npm outdated

# Update carefully and test
```

## 4. Infrastructure as Code (Terraform)

### Use Remote State for Teams

Uncomment in `terraform/provider.tf`:

```hcl
backend "s3" {
  bucket         = "your-terraform-state-bucket"
  key            = "bedrock-learning/terraform.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-state-lock"
}
```

### Version Lock Terraform Providers

Already done in `provider.tf`:

```hcl
required_providers {
  aws = {
    source  = "hashicorp/aws"
    version = "~> 5.0"  # Locks to 5.x.x
  }
}
```

### Use Variables for Configuration

Never hardcode values:

```hcl
# Bad
resource "aws_lambda_function" "example" {
  timeout = 30
}

# Good
resource "aws_lambda_function" "example" {
  timeout = var.lambda_timeout
}
```

### Tag All Resources

```hcl
tags = {
  Project     = "BedrockLearning"
  Environment = var.environment
  ManagedBy   = "Terraform"
  Owner       = "YourName"
  CostCenter  = "Learning"
}
```

## 5. Lambda Best Practices

### Set Appropriate Timeouts

```
Simple queries:  10-15 seconds
Complex tasks:   30-60 seconds
Maximum:         15 minutes
```

### Right-Size Memory

```
Light workloads: 256-512 MB
API calls:       512-1024 MB
ML inference:    1024-3008 MB
```

More memory = faster CPU but higher cost.

### Handle Errors Gracefully

```python
try:
    response = bedrock_runtime.invoke_model(...)
except ClientError as e:
    if e.response['Error']['Code'] == 'AccessDeniedException':
        # Return helpful error message
        return {'statusCode': 403, 'body': 'Bedrock access denied'}
except Exception as e:
    # Log error and return generic message
    print(f"Error: {e}")
    return {'statusCode': 500, 'body': 'Internal error'}
```

### Use Environment Variables

```python
# Don't hardcode
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

# Do this
MODEL_ID = os.environ.get('BEDROCK_MODEL_ID')
```

### Keep Lambda Package Small

```bash
# Only include necessary files
# Exclude tests, __pycache__, etc.
# This is configured in terraform/lambda.tf
```

## 6. Frontend Best Practices

### Environment-Specific Configuration

```bash
# Development
.env.local         # Local development

# Production (set in Amplify console)
NEXT_PUBLIC_API_URL=https://api.production.com
```

### Optimize Performance

```javascript
// Use React best practices
- Memoization for expensive computations
- Lazy loading for code splitting
- Image optimization (next/image)
- Static generation where possible
```

### Error Handling

```javascript
// Always handle API errors
try {
  const response = await fetch(API_URL)
  if (!response.ok) throw new Error(response.statusText)
} catch (error) {
  // Show user-friendly error message
  setError('Something went wrong. Please try again.')
}
```

### Loading States

Always show loading states during API calls to improve UX.

## 7. API Gateway Best Practices

### Enable CORS Properly

```hcl
# Configure allowed origins
Access-Control-Allow-Origin: https://yourdomain.com

# In production, don't use '*'
# Use specific domain
```

### Enable Request Validation

Add request validation in API Gateway to reject malformed requests early.

### Set Up Custom Domain

Instead of `xyz123.execute-api.us-east-1.amazonaws.com`, use `api.yourdomain.com`.

### Monitor API Usage

```bash
# CloudWatch metrics to monitor:
- Latency
- Error rate (4xx, 5xx)
- Request count
- Integration latency
```

## 8. Monitoring and Alerting

### Essential Metrics to Monitor

```
Lambda:
- Invocation count
- Error rate
- Duration
- Concurrent executions
- Throttles

API Gateway:
- 4xx errors (client errors)
- 5xx errors (server errors)
- Latency
- Request count

Bedrock:
- ModelInvocation count
- ModelInvocationClientError
- ModelInvocationServerError
```

### Set Up CloudWatch Alarms

```bash
# Example: Alert on Lambda errors
aws cloudwatch put-metric-alarm \
  --alarm-name lambda-errors \
  --alarm-description "Alert on Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold
```

### Create CloudWatch Dashboard

1. AWS Console → CloudWatch → Dashboards
2. Create dashboard
3. Add widgets for key metrics
4. Share with team

## 9. Testing Strategy

### Unit Tests

```python
# lambda/tests/test_handler.py
import pytest
from handler import lambda_handler

def test_valid_query():
    event = {"query": "What is AWS?"}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
```

### Integration Tests

```bash
# Test API endpoint
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"query": "Test query"}'
```

### End-to-End Tests

Use tools like Playwright or Cypress to test complete user flow.

## 10. Deployment Best Practices

### Use CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy infrastructure
        run: |
          cd terraform
          terraform init
          terraform apply -auto-approve
```

### Gradual Rollout

Use Lambda aliases and versions for blue-green deployments.

### Backup Before Changes

```bash
# Backup Terraform state
cp terraform.tfstate terraform.tfstate.backup

# Backup Lambda code
zip -r lambda-backup-$(date +%Y%m%d).zip lambda/
```

### Validate Before Apply

```bash
# Always run plan first
terraform plan

# Review changes carefully
# Only then apply
terraform apply
```

## 11. Documentation

### Keep README Updated

Document:
- Setup instructions
- Configuration options
- Common issues
- Contact information

### Document Architecture Decisions

Create ADR (Architecture Decision Records) for major decisions:
- Why Bedrock over SageMaker?
- Why Next.js over plain React?
- Why this Bedrock model?

### Maintain Runbooks

Document common operational tasks:
- How to deploy
- How to rollback
- How to debug issues
- How to scale

## 12. Backup and Disaster Recovery

### What to Backup

```
Critical:
- Terraform state (terraform.tfstate)
- Source code (use Git)
- Configuration files

Optional:
- CloudWatch logs (auto-retained)
- Lambda deployment packages
```

### Recovery Plan

1. Code is in Git - can redeploy anytime
2. Infrastructure is in Terraform - `terraform apply` recreates everything
3. No data to backup (stateless application)
4. Recovery time: ~10 minutes

## 13. Scaling Considerations

### Lambda Scaling

- Lambda auto-scales (1000 concurrent executions by default)
- Request increase if needed via AWS Support
- Consider reserved concurrency for critical functions

### API Gateway Scaling

- Auto-scales to handle traffic
- Default limit: 10,000 requests/second
- Can be increased via AWS Support

### Bedrock Scaling

- Managed service, scales automatically
- Monitor for throttling
- Consider provisioned throughput for high volume

## Summary Checklist

Before going to production:

- [ ] Secrets not committed to Git
- [ ] IAM roles follow least privilege
- [ ] Billing alerts configured
- [ ] Error handling implemented
- [ ] Logging enabled
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Monitoring and alarms set up
- [ ] Backup strategy defined
- [ ] CORS configured properly (not '*')
- [ ] Custom domain configured
- [ ] SSL certificate validated
- [ ] Rate limiting enabled
- [ ] Cost optimization reviewed

Following these best practices will help you build a secure, reliable, and cost-effective AWS application!
