# Git Workflow Guide

This project follows a simplified Git Flow with three types of branches:
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature development branches

## Branch Overview

```
main (production)
  └── develop (integration)
       ├── feature/add-authentication
       ├── feature/improve-ui
       └── feature/add-streaming
```

## Branch Descriptions

### main
- **Purpose**: Production-ready, stable code
- **Protected**: Direct commits not allowed
- **Updates**: Only via Pull Requests from `develop`
- **Deploys to**: Production environment

### develop
- **Purpose**: Integration branch for ongoing development
- **Protected**: Direct commits discouraged (use PRs from features)
- **Updates**: Via Pull Requests from `feature/*` branches
- **Deploys to**: Development/Staging environment

### feature/*
- **Purpose**: Individual feature development
- **Naming**: `feature/description-of-feature`
- **Created from**: `develop`
- **Merged to**: `develop` (via Pull Request)
- **Deleted after**: Merge is complete

---

## Common Workflows

### 1. Starting a New Feature

```bash
# Make sure you're on develop and it's up to date
git checkout develop
git pull origin develop

# Create a new feature branch
git checkout -b feature/your-feature-name

# Examples:
# git checkout -b feature/add-authentication
# git checkout -b feature/improve-chat-ui
# git checkout -b feature/add-rate-limiting
```

### 2. Working on a Feature

```bash
# Make your changes, then:
git add .
git commit -m "Descriptive commit message"

# Push to GitHub regularly
git push -u origin feature/your-feature-name

# Continue working
git add .
git commit -m "Another change"
git push
```

### 3. Finishing a Feature (Create Pull Request)

```bash
# Make sure your feature is up to date with develop
git checkout develop
git pull origin develop

git checkout feature/your-feature-name
git merge develop

# Resolve any conflicts, then push
git push

# Create PR on GitHub:
# Go to: https://github.com/namahaclouds/aws-bedrock-learning
# Click "Compare & pull request"
# Base: develop <- Compare: feature/your-feature-name
# Add description and create PR
```

### 4. After PR is Merged

```bash
# Switch back to develop
git checkout develop
git pull origin develop

# Delete the merged feature branch locally
git branch -d feature/your-feature-name

# Delete from GitHub (if not auto-deleted)
git push origin --delete feature/your-feature-name
```

### 5. Preparing for Production Release

```bash
# When develop is stable and ready for production
# Create PR on GitHub:
# Base: main <- Compare: develop
# Title: "Release: [version or date]"
# Get approval and merge
```

### 6. After Production Release

```bash
# Update your local main branch
git checkout main
git pull origin main

# Make sure develop is synced with main
git checkout develop
git merge main
git push origin develop
```

---

## Daily Workflow Examples

### Scenario A: Working on Frontend UI

```bash
# Start
git checkout develop
git pull origin develop
git checkout -b feature/improve-chat-interface

# Make changes to frontend/components/ChatInterface.tsx
npm run dev  # Test locally

git add frontend/
git commit -m "Improve chat interface with better styling"
git push -u origin feature/improve-chat-interface

# Create PR on GitHub when ready
# After merge, delete branch
git checkout develop
git pull origin develop
git branch -d feature/improve-chat-interface
```

### Scenario B: Adding New Lambda Function

```bash
# Start
git checkout develop
git pull origin develop
git checkout -b feature/add-bedrock-streaming

# Make changes to lambda/handler.py
# Test locally

git add lambda/
git commit -m "Add streaming support to Lambda function"
git push -u origin feature/add-bedrock-streaming

# Continue working
git add lambda/ terraform/
git commit -m "Update Terraform for streaming configuration"
git push

# Create PR when ready
```

### Scenario C: Updating Documentation

```bash
git checkout develop
git pull origin develop
git checkout -b feature/update-deployment-docs

# Edit DEPLOYMENT_GUIDE.md
git add DEPLOYMENT_GUIDE.md
git commit -m "Update deployment guide with troubleshooting section"
git push -u origin feature/update-deployment-docs

# Create PR
```

---

## Commit Message Guidelines

Use clear, descriptive commit messages:

### Good Examples ✅
```
Add user authentication with Cognito
Fix CORS error in API Gateway
Update Lambda timeout to 60 seconds
Improve error handling in chat interface
Add deployment instructions for custom domain
```

### Bad Examples ❌
```
Fixed stuff
WIP
Updates
asdf
Changed files
```

### Commit Message Format

```
<type>: <description>

[optional body]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add streaming response support to Lambda
fix: Resolve CORS error in API Gateway
docs: Update README with cost estimates
refactor: Simplify Bedrock client initialization
chore: Update dependencies to latest versions
```

---

## Branch Protection Rules (GitHub Settings)

To enforce this workflow, configure these settings on GitHub:

### For `main` branch:
1. Go to: Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require pull request before merging
   - ✅ Require approvals (1+)
   - ✅ Dismiss stale reviews when new commits are pushed
   - ✅ Require status checks to pass (if you add CI/CD)
   - ✅ Include administrators (optional)

### For `develop` branch:
1. Branch name pattern: `develop`
2. Enable:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass (if you add CI/CD)

---

## Quick Reference

### Check Current Branch
```bash
git branch
# or
git status
```

### List All Branches
```bash
# Local branches
git branch

# Remote branches
git branch -r

# All branches
git branch -a
```

### Switch Branches
```bash
git checkout branch-name

# or (newer syntax)
git switch branch-name
```

### Update Current Branch
```bash
git pull origin branch-name
```

### Delete Branch
```bash
# Local
git branch -d feature/branch-name

# Remote
git push origin --delete feature/branch-name
```

### Sync develop with main
```bash
git checkout develop
git merge main
git push origin develop
```

---

## Conflict Resolution

If you encounter merge conflicts:

```bash
# When merging develop into your feature
git checkout feature/your-feature
git merge develop

# If conflicts occur:
# 1. Open conflicted files
# 2. Look for conflict markers: <<<<<<<, =======, >>>>>>>
# 3. Manually resolve conflicts
# 4. Remove conflict markers
# 5. Test your changes

git add .
git commit -m "Resolve merge conflicts with develop"
git push
```

---

## CI/CD Integration (Future)

When you add GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches:
      - main      # Deploy to production
      - develop   # Deploy to staging

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Infrastructure
        run: |
          cd terraform
          terraform init
          terraform apply -auto-approve
```

---

## Common Questions

**Q: Can I commit directly to develop?**
A: It's discouraged. Always use feature branches and PRs for better code review and tracking.

**Q: How do I handle urgent fixes?**
A: Create a feature branch (e.g., `feature/urgent-fix-cors`) from develop, fix, and create a PR. If critical, you can fast-track the PR approval.

**Q: Should I delete feature branches after merging?**
A: Yes, always delete merged feature branches to keep the repository clean.

**Q: How often should I merge develop to main?**
A: When develop is stable and you're ready to deploy to production. This could be daily, weekly, or based on sprints.

**Q: What if I accidentally commit to develop?**
A: If not pushed yet, reset: `git reset HEAD~1`. If already pushed, create a revert commit: `git revert HEAD`.

---

## Workflow Summary

```
1. Start: develop → feature/new-feature
2. Work: Commit and push to feature branch
3. Finish: Create PR from feature → develop
4. Review: Get PR reviewed and approved
5. Merge: Merge PR to develop
6. Clean: Delete feature branch
7. Release: When ready, PR from develop → main
8. Deploy: main branch triggers production deployment
```

---

## Tools to Help

### GitHub CLI (optional)
```bash
# Install: brew install gh

# Create PR from command line
gh pr create --base develop --head feature/your-feature

# List PRs
gh pr list

# Checkout a PR locally
gh pr checkout PR_NUMBER
```

### Git Aliases (optional)
Add to `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    st = status
    cm = commit -m
    pom = push origin main
    pod = push origin develop
    pof = push origin HEAD
    feature = "!f() { git checkout develop && git pull && git checkout -b feature/$1; }; f"
```

Usage:
```bash
git feature add-authentication
# Creates and checks out feature/add-authentication from updated develop
```

---

## Need Help?

- Git documentation: https://git-scm.com/doc
- GitHub Flow guide: https://docs.github.com/en/get-started/quickstart/github-flow
- Contact the team lead if you have questions

---

**Remember**:
- `main` = Production (stable, working code)
- `develop` = Integration (tested features ready for release)
- `feature/*` = Work in progress (your current development)

Happy coding! 🚀
