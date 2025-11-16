# AWS Bedrock Learning Project

## Project Overview
A full-stack web application built to learn AWS services, featuring:
- Next.js frontend hosted on AWS Amplify
- Python Lambda function using Amazon Bedrock for AI-powered queries
- Infrastructure as Code using Terraform
- Custom domain from GoDaddy

## Architecture

```
User Browser
    ↓
GoDaddy Domain → AWS Route 53
    ↓
AWS Amplify (Next.js Frontend)
    ↓
API Gateway
    ↓
AWS Lambda (Python)
    ↓
Amazon Bedrock (AI Model)
```

## Tech Stack
- **Frontend**: Next.js (React framework)
- **Backend**: Python Lambda functions
- **AI/ML**: Amazon Bedrock
- **Hosting**: AWS Amplify
- **Infrastructure**: Terraform
- **Domain**: GoDaddy (linked via Route 53)

## Project Structure

```
awsbedrock/
├── Claude.md                 # This file - project context
├── README.md                 # User-facing documentation
├── terraform/                # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── iam.tf               # IAM roles and policies
│   ├── lambda.tf            # Lambda configuration
│   ├── api-gateway.tf       # API Gateway setup
│   ├── amplify.tf           # Amplify hosting
│   └── route53.tf           # Domain configuration
├── frontend/                 # Next.js application
│   ├── package.json
│   ├── next.config.js
│   ├── pages/
│   ├── components/
│   └── public/
├── lambda/                   # Python Lambda functions
│   ├── requirements.txt
│   ├── handler.py           # Main Lambda handler
│   ├── bedrock_client.py    # Bedrock integration
│   └── tests/
└── venv/                     # Python virtual environment (gitignored)
```

## AWS Services Used

1. **AWS Amplify**: Hosts the Next.js frontend with CI/CD
2. **AWS Lambda**: Serverless compute for backend logic
3. **Amazon Bedrock**: AI/ML service for processing queries
4. **API Gateway**: RESTful API endpoint for frontend-backend communication
5. **IAM**: Identity and access management for secure resource access
6. **Route 53**: DNS service to connect GoDaddy domain
7. **CloudWatch**: Logging and monitoring

## Development Setup

### Prerequisites
- AWS CLI installed and configured (`aws configure`)
- Terraform installed
- Node.js and npm installed
- Python 3.x installed
- Git for version control

### Local Environment
- Use Python virtual environment (venv) for Lambda development
- Node modules for Next.js frontend
- Terraform for infrastructure provisioning

## IAM Permissions Required

The IAM user needs permissions for:
- Amplify (full access for app creation and deployment)
- Lambda (create, update, invoke functions)
- Bedrock (invoke model permissions)
- API Gateway (create and manage APIs)
- IAM (create roles for Lambda execution)
- Route 53 (manage DNS records)
- CloudWatch Logs (for monitoring)

## Bedrock Model Selection

Recommended models for simple queries:
- **Claude 3 Haiku**: Fast, cost-effective for simple queries
- **Claude 3 Sonnet**: Balanced performance and capability
- Model ID format: `anthropic.claude-3-haiku-20240307-v1:0`

## Terraform State Management

- **Initial Setup**: Local state file (terraform.tfstate)
- **Best Practice**: Consider moving to S3 backend with DynamoDB locking for production
- Keep state file secure - contains sensitive information

## Environment Variables

### Lambda Function
- `BEDROCK_MODEL_ID`: The Bedrock model to use
- `AWS_REGION`: AWS region for Bedrock (us-east-1 or us-west-2)

### Frontend (Next.js)
- `NEXT_PUBLIC_API_URL`: API Gateway endpoint URL

## Deployment Workflow

1. **Infrastructure**: `terraform apply` to create AWS resources
2. **Lambda**: Terraform packages and deploys Lambda function
3. **Frontend**: Push to Amplify-connected Git repo or manual deployment
4. **Domain**: Configure GoDaddy nameservers to point to Route 53

## Security Best Practices

1. Never commit AWS credentials to Git
2. Use IAM roles with least privilege principle
3. Enable CloudWatch logging for debugging
4. Use environment variables for sensitive configuration
5. Implement API rate limiting in API Gateway
6. Enable CORS properly for frontend-backend communication

## Cost Optimization

- Use Bedrock on-demand pricing (pay per request)
- Lambda free tier: 1M requests/month
- Amplify: Pay for build minutes and hosting
- Monitor costs via AWS Cost Explorer

## Testing Strategy

1. **Local Lambda Testing**: Use AWS SAM or mock Bedrock responses
2. **Frontend Testing**: Next.js local development server
3. **Integration Testing**: Test API Gateway endpoints
4. **End-to-End**: Test complete user flow after deployment

## Common Issues & Solutions

### Issue: Lambda timeout calling Bedrock
- Solution: Increase Lambda timeout (default 3s → 30s)

### Issue: CORS errors from frontend
- Solution: Configure API Gateway CORS settings

### Issue: Bedrock access denied
- Solution: Ensure Lambda execution role has bedrock:InvokeModel permission

### Issue: Domain not connecting
- Solution: Verify Route 53 hosted zone and GoDaddy nameservers match

## Next Steps After Initial Deployment

1. Add user authentication (Cognito)
2. Implement caching (DynamoDB or ElastiCache)
3. Add monitoring dashboards (CloudWatch)
4. Set up CI/CD pipeline
5. Implement error handling and retries
6. Add automated tests

## Learning Resources

- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/
- Next.js Documentation: https://nextjs.org/docs
- AWS Amplify Hosting: https://docs.aws.amazon.com/amplify/

## Development Notes

- Region selection: Choose region where Bedrock is available (us-east-1, us-west-2, etc.)
- Bedrock models require access request approval in AWS Console
- Keep Terraform state file backed up
- Test locally before deploying to AWS to minimize costs
