# Route 53 for Custom Domain (GoDaddy)

# Create hosted zone for custom domain
resource "aws_route53_zone" "main" {
  count = var.domain_name != "" ? 1 : 0
  name  = var.domain_name

  tags = {
    Name = "${var.project_name}-hosted-zone"
  }
}

# Output nameservers for GoDaddy configuration
output "route53_name_servers" {
  description = "Name servers to configure in GoDaddy"
  value       = var.domain_name != "" ? aws_route53_zone.main[0].name_servers : []
}

output "route53_zone_id" {
  description = "Route 53 Hosted Zone ID"
  value       = var.domain_name != "" ? aws_route53_zone.main[0].zone_id : ""
}

# Instructions output
output "domain_setup_instructions" {
  description = "Instructions for setting up custom domain"
  value = var.domain_name != "" ? join("\n", [
    "",
    "=== DOMAIN SETUP INSTRUCTIONS ===",
    "",
    "1. Log into your GoDaddy account",
    "2. Navigate to DNS Management for domain: ${var.domain_name}",
    "3. Change nameservers to the following Route 53 nameservers:",
    join("\n", [for ns in aws_route53_zone.main[0].name_servers : "   ${ns}"]),
    "",
    "4. In AWS Amplify Console:",
    "   - Go to your Amplify app",
    "   - Navigate to Domain Management",
    "   - Verify the domain is properly configured",
    "   - Wait for SSL certificate provisioning",
    "",
    "5. DNS propagation can take up to 48 hours (usually much faster)",
    "",
    "Test your domain with: dig ${var.domain_name}",
    ""
  ]) : "No custom domain configured. Set 'domain_name' variable to enable."
}
