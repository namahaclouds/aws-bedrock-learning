# Git Flow Quick Reference

## Branch Structure
```
main (production) ← develop (integration) ← feature/* (development)
```

## Starting New Work

```bash
# Always start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name
```

## While Working

```bash
# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push -u origin feature/your-feature-name  # First time
git push                                        # Subsequent pushes
```

## Creating Pull Request

1. Push your feature branch
2. Go to GitHub repository
3. Click "Compare & pull request"
4. Set: `develop ← feature/your-feature-name`
5. Fill in description
6. Create pull request

## After PR is Merged

```bash
# Update develop
git checkout develop
git pull origin develop

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## Production Release

```bash
# Create PR on GitHub: main ← develop
# After merge:
git checkout main
git pull origin main
git checkout develop
git merge main
git push origin develop
```

## Daily Commands

```bash
# Check current branch
git status

# See all branches
git branch -a

# Switch branches
git checkout branch-name

# Update current branch
git pull
```

## Common Feature Names

```bash
feature/add-authentication
feature/improve-ui
feature/fix-cors-error
feature/add-rate-limiting
feature/update-docs
feature/refactor-lambda
```

## Need Help?

See full guide: `GIT_WORKFLOW.md`
