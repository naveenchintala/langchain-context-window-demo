#!/bin/bash

# Script to create GitHub repository and push code
# Usage: ./setup_github_repo.sh <repo-name> [description]

REPO_NAME="${1:-langchain-context-window-demo}"
DESCRIPTION="${2:-Demonstration of context window problem in LLMs using LangChain}"

echo "Setting up GitHub repository: $REPO_NAME"
echo "Description: $DESCRIPTION"
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI..."
    gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source=. --remote=origin --push
    echo ""
    echo "✅ Repository created and code pushed!"
    echo "View at: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
else
    echo "GitHub CLI not found. Using GitHub API..."
    echo ""
    
    # Check for GitHub token
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "⚠️  GITHUB_TOKEN environment variable not set."
        echo ""
        echo "To create the repository, you have two options:"
        echo ""
        echo "Option 1: Use GitHub CLI (recommended)"
        echo "  1. Install: brew install gh"
        echo "  2. Authenticate: gh auth login"
        echo "  3. Run this script again"
        echo ""
        echo "Option 2: Create manually on GitHub"
        echo "  1. Go to https://github.com/new"
        echo "  2. Repository name: $REPO_NAME"
        echo "  3. Description: $DESCRIPTION"
        echo "  4. Choose public/private"
        echo "  5. Don't initialize with README (we already have one)"
        echo "  6. Click 'Create repository'"
        echo "  7. Then run these commands:"
        echo "     git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
        echo "     git branch -M main"
        echo "     git push -u origin main"
        echo ""
        echo "Option 3: Use GitHub API with token"
        echo "  1. Get a token from: https://github.com/settings/tokens"
        echo "  2. Export it: export GITHUB_TOKEN=your_token_here"
        echo "  3. Run this script again"
        exit 1
    fi
    
    # Get GitHub username
    USERNAME=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep -o '"login":"[^"]*' | cut -d'"' -f4)
    
    if [ -z "$USERNAME" ]; then
        echo "❌ Failed to authenticate with GitHub. Check your token."
        exit 1
    fi
    
    echo "Authenticated as: $USERNAME"
    echo "Creating repository..."
    
    # Create repository via API
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$REPO_NAME\",\"description\":\"$DESCRIPTION\",\"public\":true}")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" = "201" ]; then
        echo "✅ Repository created successfully!"
        
        # Add remote and push
        git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || \
        git remote set-url origin "https://github.com/$USERNAME/$REPO_NAME.git"
        
        git branch -M main
        git push -u origin main
        
        echo ""
        echo "✅ Code pushed to GitHub!"
        echo "View at: https://github.com/$USERNAME/$REPO_NAME"
    else
        echo "❌ Failed to create repository. HTTP Code: $HTTP_CODE"
        echo "Response: $BODY"
        exit 1
    fi
fi

