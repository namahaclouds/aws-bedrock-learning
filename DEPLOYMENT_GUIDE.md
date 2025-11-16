# AWS Bedrock Project - Step-by-Step Deployment Guide

This guide will walk you through deploying your complete AWS Bedrock application from scratch.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] AWS Account with billing enabled
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] Terraform installed (`terraform --version`)
- [ ] Node.js and npm installed (`node --version`)
- [ ] Python 3.x installed (`python3 --version`)
- [ ] GoDaddy domain (optional, for custom domain)
- [ ] Basic knowledge of terminal/command line

## Phase 1: Enable Amazon Bedrock Access

This MUST be done before deploying infrastructure.

### Step 1.1: Request Bedrock Model Access

1. Log into AWS Console: https://console.aws.amazon.com
2. Navigate to **Amazon Bedrock** service
3. In the left sidebar, click **Model access**
4. Click **Modify model access** button
5. Check the box for:
   - **Claude 3 Haiku** (recommended for learning - fast and cheap)
   - **Claude 3 Sonnet** (optional - more capable)
6. Click **Request model access**
7. Wait for approval (usually instant)
8. Verify status shows "Access granted"

### Step 1.2: Verify Bedrock Access Locally

```bash
# Activate Python virtual environment
source venv/bin/activate

# Run test script
python lambda/test_bedrock.py
```

If successful, you should see: "✓ SUCCESS! Bedrock is working correctly!"

If you get errors:
- **AccessDeniedException**: Go back to Step 1.1
- **ResourceNotFoundException**: Check your AWS region
- **Credentials error**: Run `aws configure` to set up credentials

## Phase 2: Configure Your Project

### Step 2.1: Set Up Terraform Variables

```bash
cd terraform

# Copy example variables file
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your settings
```

Minimum configuration in `terraform.tfvars`:

```hcl
aws_region   = "us-east-1"  # or us-west-2 where Bedrock is available
project_name = "bedrock-learning"
environment  = "dev"

# Optional: Add your domain if you have one
# domain_name = "example.com"
```

### Step 2.2: Review AWS Credentials

```bash
# Verify your AWS credentials work
aws sts get-caller-identity

# Should show your AWS account ID, user ARN, etc.
```

## Phase 3: Deploy Infrastructure with Terraform

### Step 3.1: Initialize Terraform

```bash
cd terraform

# Initialize Terraform (downloads providers)
terraform init
```

Expected output: "Terraform has been successfully initialized!"

### Step 3.2: Review the Deployment Plan

```bash
# See what will be created
terraform plan
```

Review the plan. You should see resources being created:
- IAM roles and policies
- Lambda function
- API Gateway
- Amplify app
- Route 53 hosted zone (if domain_name is set)
- CloudWatch log groups

### Step 3.3: Deploy Infrastructure

```bash
# Deploy everything
terraform apply

# Type 'yes' when prompted
```

This will take 2-5 minutes. When complete, you'll see outputs including:
- API Gateway URL
- Amplify app URL
- Lambda function name

**IMPORTANT**: Save these outputs! You'll need them.

### Step 3.4: Save Important URLs

```bash
# View outputs again anytime with:
terraform output

# Save to a file for reference
terraform output > ../deployment-outputs.txt
```

## Phase 4: Test the Backend API

Before deploying the frontend, verify your backend works.

### Step 4.1: Test API Endpoint

```bash
# Get your API URL from Terraform output
API_URL=$(cd terraform && terraform output -raw api_gateway_url)

# Test the endpoint
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AWS in one sentence?"}'
```

Expected response:
```json
{
  "query": "What is AWS in one sentence?",
  "response": "Amazon Web Services (AWS) is...",
  "model": "anthropic.claude-3-haiku-20240307-v1:0"
}
```

### Step 4.2: Troubleshooting Backend Issues

If the test fails:

**Error: "Access denied"**
- Check Lambda execution role has Bedrock permissions
- Run: `cd terraform && terraform apply` again

**Error: "Internal server error"**
- Check Lambda logs: `aws logs tail /aws/lambda/bedrock-learning-query-function --follow`
- Verify Bedrock access was granted in Phase 1

**Error: "Connection refused" or timeout**
- Verify API Gateway was created: `aws apigateway get-rest-apis`
- Check your internet connection

## Phase 5: Deploy Frontend Application

### Step 5.1: Install Frontend Dependencies

```bash
cd frontend

# Install all dependencies
npm install
```

This will take 1-3 minutes.

### Step 5.2: Configure API URL

```bash
# Copy example environment file
cp .env.local.example .env.local

# Get API URL from Terraform
cd ../terraform
API_URL=$(terraform output -raw api_gateway_url)
echo $API_URL

# Edit frontend/.env.local and set:
# NEXT_PUBLIC_API_URL=<paste your API URL here>
```

Or do it in one command:

```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=$(cd ../terraform && terraform output -raw api_gateway_url)" > .env.local
```

### Step 5.3: Test Frontend Locally

```bash
cd frontend

# Run development server
npm run dev
```

Open http://localhost:3000 in your browser.

Try asking a question like "What is machine learning?"

If it works locally, you're ready to deploy!

Press Ctrl+C to stop the dev server.

### Step 5.4: Build Frontend for Production

```bash
cd frontend

# Create production build
npm run build

# This creates an 'out' folder with static files
```

## Phase 6: Deploy to AWS Amplify

You have two deployment options:

### Option A: Manual Deployment (Recommended for Learning)

1. Go to AWS Console → AWS Amplify
2. Click **Create new app** → **Deploy without Git**
3. App name: `bedrock-frontend`
4. Drag and drop the `frontend/out` folder
5. Click **Save and deploy**
6. Wait 2-3 minutes for deployment
7. Click the provided URL to access your app!

### Option B: GitHub Deployment (For Continuous Deployment)

1. Push your code to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/yourrepo.git
git push -u origin main
```

2. Go to AWS Console → AWS Amplify
3. Click **Create new app** → **Host web app**
4. Choose **GitHub**
5. Authorize AWS Amplify
6. Select your repository and branch
7. Build settings are already configured in `amplify.tf`
8. Click **Save and deploy**

## Phase 7: Connect Custom Domain (Optional)

Only if you set `domain_name` in terraform.tfvars.

### Step 7.1: Get Route 53 Nameservers

```bash
cd terraform

# Get nameservers
terraform output route53_name_servers
```

Copy these 4 nameserver addresses.

### Step 7.2: Update GoDaddy DNS

1. Log into GoDaddy: https://dnsmanagement.godaddy.com
2. Select your domain
3. Click **Nameservers** → **Change**
4. Select **Custom nameservers**
5. Paste the 4 Route 53 nameservers
6. Save changes

### Step 7.3: Wait for DNS Propagation

```bash
# Check if DNS has propagated (may take up to 48 hours)
dig yourdomain.com

# Or use online tool: https://www.whatsmydns.net
```

### Step 7.4: Configure SSL in Amplify

1. Go to AWS Amplify Console
2. Select your app
3. Go to **Domain management**
4. Your domain should show up
5. Wait for SSL certificate to be issued (automatic, takes 5-10 minutes)
6. Once status is "Available", your site is live!

## Phase 8: Verification and Testing

### Step 8.1: Access Your Application

Your app is now live at:
- Amplify URL: `https://main.xxxxx.amplifyapp.com`
- Custom domain: `https://yourdomain.com` (if configured)

### Step 8.2: End-to-End Test

1. Open your application URL
2. Type a question: "Explain serverless computing"
3. Click **Send**
4. You should get a response from Claude within 1-3 seconds
5. Try multiple questions to verify it works consistently

### Step 8.3: Monitor Logs

```bash
# Watch Lambda logs in real-time
aws logs tail /aws/lambda/bedrock-learning-query-function --follow

# In another terminal, use your app to see logs appear
```

## Phase 9: Understanding Costs

### Expected Monthly Costs (Light Usage)

- **Lambda**: $0 (within free tier for 1M requests/month)
- **API Gateway**: $0-5 (first 1M requests free)
- **Amplify Hosting**: $0.01/GB storage + $0.15/GB served
- **Bedrock (Claude Haiku)**: ~$0.001 per request
- **Route 53**: $0.50/month (per hosted zone)

**Estimated total for learning**: $1-10/month

### Monitor Your Costs

1. AWS Console → Billing Dashboard
2. Set up billing alerts:
   - Click **Budgets**
   - Create budget
   - Set alert at $10

## Common Issues and Solutions

### Issue: "Function timed out"

**Solution**: Increase Lambda timeout

```bash
# Edit terraform/variables.tf
# Change lambda_timeout = 30 to lambda_timeout = 60

cd terraform
terraform apply
```

### Issue: CORS errors in browser

**Solution**: CORS is configured in Lambda handler.py. Verify:
- `Access-Control-Allow-Origin: '*'` is in response headers
- API Gateway OPTIONS method exists

### Issue: Amplify build fails

**Solution**:
1. Check build logs in Amplify console
2. Verify `package.json` has correct dependencies
3. Try local build: `cd frontend && npm run build`

### Issue: High costs

**Solution**:
1. Check AWS Cost Explorer
2. Verify you're not in a request loop
3. Consider switching to smaller Bedrock model
4. Delete resources when not in use: `terraform destroy`

## Cleanup (When Done Learning)

To avoid ongoing charges:

```bash
# Destroy all resources
cd terraform
terraform destroy

# Type 'yes' to confirm
```

This will delete:
- Lambda function
- API Gateway
- Amplify app
- Route 53 hosted zone
- All IAM roles

**Note**: Amplify apps might need manual deletion from the console.

## Next Steps

Now that your app is running:

1. **Add features**:
   - Conversation history
   - User authentication (Cognito)
   - Save conversations to DynamoDB
   - Rate limiting

2. **Improve UX**:
   - Streaming responses
   - Markdown formatting
   - Code syntax highlighting

3. **Production readiness**:
   - Environment-specific configs
   - Terraform remote state (S3)
   - CI/CD pipeline
   - Monitoring and alerts

4. **Learn more**:
   - Different Bedrock models
   - Fine-tuning
   - RAG (Retrieval Augmented Generation)

## Getting Help

If you encounter issues:

1. Check CloudWatch logs for errors
2. Review Terraform outputs
3. Verify all prerequisites are met
4. Check AWS service quotas
5. Review AWS documentation

## Congratulations!

You've successfully deployed a full-stack serverless AI application using:
- Amazon Bedrock for AI
- AWS Lambda for compute
- API Gateway for APIs
- AWS Amplify for hosting
- Terraform for infrastructure

This is production-ready architecture used by many companies!
