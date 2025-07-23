# GitHub Personal Access Token Configuration

## Token Details
- **Name**: PR Analytics Dashboard
- **Created**: Before repo setup
- **Expiration**: No expiration date
- **Scope**: repo (full access to private repositories)
- **Purpose**: Access private repository `axel-springer-kugawana/aviv_data_collection_contracts`

## Repository Secret Configuration
- **Secret Name**: `PERSONAL_ACCESS_TOKEN`
- **Used in**: `.github/workflows/daily-update.yml`
- **Environment Variable**: `GITHUB_TOKEN`

## Why Personal Access Token is Required
The default `GITHUB_TOKEN` provided by GitHub Actions can only access the current repository. Since our PR analytics needs to fetch data from a private repository (`axel-springer-kugawana/aviv_data_collection_contracts`), we need a Personal Access Token with `repo` scope.

## Security Notes
1. The token has no expiration date - consider setting expiration for better security
2. Token is stored as encrypted secret in repository settings
3. Never commit the token directly in code
4. Use `${{ secrets.PERSONAL_ACCESS_TOKEN }}` in workflows

## Troubleshooting
If the workflow fails with 404 errors:
1. Verify the token has `repo` scope
2. Check if the token is added as repository secret
3. Ensure the target repository name is correct
4. Verify you have access to the target repository

## Token Management
- To view tokens: Settings → Developer settings → Personal access tokens → Tokens (classic)
- To regenerate: Click on token name → Regenerate token
- To add to repo: Repository Settings → Secrets and variables → Actions → New repository secret
