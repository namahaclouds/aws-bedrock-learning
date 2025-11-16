# AWS Bedrock Learning Project

A full-stack serverless application using AWS Amplify, Lambda, and Bedrock with Terraform for infrastructure management.

## Quick Start Guide

Follow these steps in order to set up and deploy your project.

### Step 1: Enable Amazon Bedrock Access

Before you begin, you need to request access to Bedrock models:

1. Log into AWS Console
2. Navigate to Amazon Bedrock service
3. Go to "Model access" in the left sidebar
4. Request access to Claude models (Haiku or Sonnet recommended)
5. Wait for approval (usually instant for most models)

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install AWS SDK and dependencies
pip install boto3 pytest
```

### Step 3: Verify AWS Configuration

```bash
# Check your AWS credentials are configured
aws sts get-caller-identity

# Note your AWS region - Bedrock is available in specific regions
# Recommended: us-east-1 or us-west-2
aws configure get region
```

### Step 4: Initialize Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Review the plan (see what will be created)
terraform plan

# Apply the configuration (type 'yes' when prompted)
terraform apply
```

This will create:
- IAM roles for Lambda
- Lambda function
- API Gateway
- Amplify app
- Route 53 hosted zone (for domain)

### Step 5: Set Up Next.js Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run locally to test
npm run dev

# Open http://localhost:3000 in your browser
```

### Step 6: Deploy to Amplify

Option A: Connect Git Repository
1. Push your code to GitHub
2. In AWS Console, go to Amplify
3. Connect your repository
4. Configure build settings (already in amplify.yml)
5. Deploy

Option B: Manual Deployment
```bash
cd frontend
npm run build

# Use Amplify CLI or console to deploy the build
```

### Step 7: Configure Custom Domain

1. Get Route 53 nameservers from Terraform output
2. Log into GoDaddy
3. Go to DNS Management for your domain
4. Update nameservers to Route 53 nameservers
5. Wait for DNS propagation (up to 48 hours, usually much faster)

### Step 8: Test Your Application

1. Open your Amplify app URL (from Terraform output or AWS Console)
2. Enter a query in the UI
3. The query should be sent to Lambda → Bedrock → return response

## Project Architecture

```
User → GoDaddy Domain → Route 53 → Amplify (Next.js)
                                        ↓
                                   API Gateway
                                        ↓
                                   Lambda (Python)
                                        ↓
                                   Amazon Bedrock
```

## Development Workflow

### Making Changes to Lambda

```bash
# Activate virtual environment
source venv/bin/activate

# Edit lambda/handler.py

# Test locally (optional)
cd lambda
python handler.py

# Deploy changes
cd ../terraform
terraform apply
```

### Making Changes to Frontend

```bash
cd frontend

# Make your changes

# Test locally
npm run dev

# Commit and push (if using Git with Amplify)
git add .
git commit -m "Your changes"
git push

# Amplify will automatically rebuild and deploy
```

## Useful Commands

### Terraform

```bash
# See current infrastructure
terraform show

# Destroy all resources (be careful!)
terraform destroy

# View outputs (API URL, Amplify URL, etc.)
terraform output
```

### AWS CLI

```bash
# Test Lambda function directly
aws lambda invoke \
  --function-name bedrock-query-function \
  --payload '{"query": "What is AWS?"}' \
  response.json

# View Lambda logs
aws logs tail /aws/lambda/bedrock-query-function --follow

# Check Amplify apps
aws amplify list-apps
```

### Testing Bedrock Access

```bash
# Activate venv first
source venv/bin/activate

# Test Bedrock from command line
python lambda/test_bedrock.py
```

## Environment Variables

### Lambda (set via Terraform)
- `BEDROCK_MODEL_ID`: Model to use (e.g., anthropic.claude-3-haiku-20240307-v1:0)
- `AWS_REGION`: Region for Bedrock

### Frontend (create .env.local)
```
NEXT_PUBLIC_API_URL=https://your-api-gateway-url.amazonaws.com/prod
```

## Troubleshooting

### Lambda returns "Access Denied" for Bedrock
- Ensure you've requested Bedrock model access in AWS Console
- Verify Lambda execution role has bedrock:InvokeModel permission
- Check the region matches where Bedrock is available

### CORS errors in browser
- Verify API Gateway has CORS enabled
- Check allowed origins include your Amplify domain

### Terraform errors
- Run `terraform init` if provider errors occur
- Check AWS credentials: `aws sts get-caller-identity`
- Ensure IAM user has sufficient permissions

### Domain not working
- Verify nameservers in GoDaddy match Route 53
- DNS propagation can take up to 48 hours
- Use `dig` or `nslookup` to check DNS resolution

## Cost Estimate

For development/learning (assuming light usage):
- Lambda: ~$0 (within free tier)
- API Gateway: ~$0-5/month
- Amplify: ~$0-15/month
- Bedrock: ~$0.001 per request (Haiku)
- Route 53: ~$0.50/month per hosted zone

Total: ~$1-20/month for light development usage

## Security Best Practices

1. Never commit `.env` files or AWS credentials
2. Use IAM roles instead of hardcoded credentials
3. Enable CloudWatch logging for debugging
4. Implement rate limiting on API Gateway
5. Use HTTPS only (enforced by Amplify/API Gateway)

## Next Steps

Once you have the basic setup working:
- [ ] Add error handling in Lambda
- [ ] Implement loading states in frontend
- [ ] Add Cognito for user authentication
- [ ] Store conversation history in DynamoDB
- [ ] Add CloudWatch dashboards
- [ ] Set up alerts for errors
- [ ] Implement CI/CD pipeline
- [ ] Add unit tests

## Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/)
- [Next.js Documentation](https://nextjs.org/docs)
- [AWS Amplify Hosting Guide](https://docs.aws.amazon.com/amplify/)

## Support

For issues or questions:
1. Check CloudWatch logs for Lambda errors
2. Review Terraform output for resource URLs
3. Consult AWS documentation
4. Check AWS service quotas and limits

## License

This is a personal learning project.
