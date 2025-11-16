# Consolidated Outputs

# Quick Start Summary
output "quick_start_summary" {
  description = "Quick start guide with all important URLs and next steps"
  value       = <<-EOT

    ╔═══════════════════════════════════════════════════════════════╗
    ║         AWS BEDROCK PROJECT - DEPLOYMENT COMPLETE             ║
    ╚═══════════════════════════════════════════════════════════════╝

    📍 IMPORTANT URLs:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Frontend (Amplify):
      ${aws_amplify_app.frontend.default_domain}

    API Endpoint:
      ${aws_api_gateway_stage.api_stage.invoke_url}/query

    Lambda Function:
      ${aws_lambda_function.bedrock_query.function_name}

    ${var.domain_name != "" ? "Custom Domain: ${var.domain_name}" : ""}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📋 NEXT STEPS:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    1. Test your API:
       curl -X POST ${aws_api_gateway_stage.api_stage.invoke_url}/query \
         -H "Content-Type: application/json" \
         -d '{"query": "What is AWS?"}'

    2. Deploy Frontend:
       cd frontend
       npm install
       npm run build

       Then either:
       - Push to GitHub (if connected to Amplify)
       - Manual deploy via AWS Console

    3. Update Frontend API URL:
       Create frontend/.env.local with:
       NEXT_PUBLIC_API_URL=${aws_api_gateway_stage.api_stage.invoke_url}

    ${var.domain_name != "" ? "\n    4. Configure GoDaddy nameservers (see domain_setup_instructions output)" : ""}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔍 MONITORING & DEBUGGING:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    View Lambda Logs:
      aws logs tail /aws/lambda/${aws_lambda_function.bedrock_query.function_name} --follow

    Test Lambda Directly:
      aws lambda invoke \
        --function-name ${aws_lambda_function.bedrock_query.function_name} \
        --payload '{"query": "Hello Bedrock"}' \
        response.json

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  EOT
}
