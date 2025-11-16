# Quick Start Guide

Get your AWS Bedrock app running in 15 minutes!

## Prerequisites

- AWS account with AWS CLI configured (`aws configure`)
- Terraform installed
- Node.js and Python 3 installed

## Step 1: Enable Bedrock Access (2 minutes)

1. AWS Console → Amazon Bedrock → Model access
2. Click "Modify model access"
3. Enable "Claude 3 Haiku"
4. Click "Request model access"

## Step 2: Test Bedrock Locally (1 minute)

```bash
# Activate virtual environment
source venv/bin/activate

# Test Bedrock access
python lambda/test_bedrock.py
```

Should see: "✓ SUCCESS!"

## Step 3: Deploy Infrastructure (5 minutes)

```bash
cd terraform

# Copy and edit config
cp terraform.tfvars.example terraform.tfvars
# (Use defaults or edit aws_region if needed)

# Deploy
terraform init
terraform apply  # Type 'yes' when prompted

# Save the API URL shown in outputs
```

## Step 4: Test Backend (1 minute)

```bash
# Get API URL from terraform output and test
API_URL=$(terraform output -raw api_gateway_url)

curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AWS?"}'
```

Should get a JSON response with Claude's answer.

## Step 5: Deploy Frontend (5 minutes)

```bash
cd ../frontend

# Install and configure
npm install

# Set API URL
echo "NEXT_PUBLIC_API_URL=$(cd ../terraform && terraform output -raw api_gateway_url)" > .env.local

# Test locally
npm run dev
# Open http://localhost:3000 and try asking a question

# Build for production
npm run build
```

## Step 6: Deploy to Amplify (2 minutes)

1. AWS Console → AWS Amplify
2. "Create new app" → "Deploy without Git"
3. Drag and drop `frontend/out` folder
4. Click "Save and deploy"
5. Wait ~2 minutes
6. Open the Amplify URL and test!

## Done!

Your app is live. Try it out!

## Optional: Custom Domain

If you have a GoDaddy domain:

1. Set `domain_name = "yourdomain.com"` in `terraform/terraform.tfvars`
2. Run `terraform apply` again
3. Copy the nameservers from output
4. Update nameservers in GoDaddy DNS settings
5. Wait 10-60 minutes for DNS propagation

## Cleanup

When done learning:

```bash
cd terraform
terraform destroy  # Type 'yes' to confirm
```

## Troubleshooting

**Lambda timeout?** Increase `lambda_timeout` in `terraform/variables.tf`

**CORS errors?** Already configured, check API URL is correct in `.env.local`

**Bedrock access denied?** Go back to Step 1, ensure model access is granted

**Need help?** Check `DEPLOYMENT_GUIDE.md` for detailed instructions

## Cost

Expected cost for learning: $1-10/month
- Most services have free tier
- Bedrock charges ~$0.001 per request
- Set up billing alerts at $10

## What You Built

- Serverless AI chat app
- Next.js frontend on AWS Amplify
- Python Lambda with Amazon Bedrock
- API Gateway for REST API
- Full infrastructure as code with Terraform

Congratulations! 🎉
