# Remove Secrets from Git History

GitHub detected your tokens in config/.env. We need to remove them from the git history.

## Option 1: Quick Fix (Recommended)
Remove the config folder from the repository entirely:

```bash
# Remove config folder from git
git rm -r --cached config/
echo "config/" >> .gitignore

# Commit the changes
git add .gitignore
git commit -m "fix: remove config folder with secrets"

# Now we need to remove it from history
git filter-branch --force --index-filter 'git rm -r --cached --ignore-unmatch config/' --prune-empty --tag-name-filter cat -- --all

# Force push (this rewrites history)
git push origin main --force
```

## Option 2: Interactive Rebase (More Complex)
If Option 1 doesn't work:

```bash
# Find the commit with secrets
git log --oneline | head -20

# Interactive rebase from before the bad commit
git rebase -i HEAD~5  # Adjust number based on where the commit is

# In the editor, change 'pick' to 'edit' for the commit with secrets
# Save and exit

# Remove the config folder
git rm -r config/
git commit --amend

# Continue rebase
git rebase --continue

# Force push
git push origin main --force
```

## IMPORTANT: After fixing this
1. The tokens in config/.env are now exposed and should be considered compromised
2. You should regenerate your GitHub token immediately
3. Update your local .env file with the new token
4. Never commit .env files to git

## Prevent Future Issues
Make sure .gitignore includes:
```
.env
config/
*.env
```
