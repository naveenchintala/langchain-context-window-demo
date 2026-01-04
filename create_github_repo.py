#!/usr/bin/env python3
"""
Script to create a GitHub repository and push the code
"""

import os
import subprocess
import sys
import json

REPO_NAME = "langchain-context-window-demo"
DESCRIPTION = "Demonstration of context window problem in LLMs using LangChain"

def check_github_cli():
    """Check if GitHub CLI is installed and authenticated"""
    try:
        result = subprocess.run(['gh', 'auth', 'status'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_with_gh_cli():
    """Create repo using GitHub CLI"""
    print("Using GitHub CLI to create repository...")
    try:
        subprocess.run(['gh', 'repo', 'create', REPO_NAME, 
                       '--public', 
                       '--description', DESCRIPTION,
                       '--source', '.',
                       '--remote', 'origin',
                       '--push'], check=True)
        print(f"✅ Repository created and pushed!")
        username = subprocess.run(['gh', 'api', 'user', '--jq', '.login'],
                                 capture_output=True, text=True).stdout.strip()
        print(f"View at: https://github.com/{username}/{REPO_NAME}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def create_with_api():
    """Create repo using GitHub API"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        return False
    
    import urllib.request
    import urllib.error
    
    url = 'https://api.github.com/user/repos'
    data = json.dumps({
        'name': REPO_NAME,
        'description': DESCRIPTION,
        'public': True
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            repo_data = json.loads(response.read())
            username = repo_data['owner']['login']
            
            # Add remote and push
            subprocess.run(['git', 'remote', 'add', 'origin', 
                          f'https://github.com/{username}/{REPO_NAME}.git'],
                         capture_output=True)
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
            
            print(f"✅ Repository created and pushed!")
            print(f"View at: https://github.com/{username}/{REPO_NAME}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ Error creating repository: {e.code}")
        print(f"Response: {error_body}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("GitHub Repository Setup")
    print("=" * 60)
    print(f"Repository name: {REPO_NAME}")
    print(f"Description: {DESCRIPTION}")
    print()
    
    # Try GitHub CLI first
    if check_github_cli():
        if create_with_gh_cli():
            return
        print("\nGitHub CLI failed, trying API...\n")
    
    # Try API
    if create_with_api():
        return
    
    # Manual instructions
    print("\n" + "=" * 60)
    print("Manual Setup Instructions")
    print("=" * 60)
    print("\nOption 1: Use GitHub CLI (Recommended)")
    print("  1. Install: brew install gh")
    print("  2. Authenticate: gh auth login")
    print("  3. Run: python3 create_github_repo.py")
    print("\nOption 2: Create on GitHub Website")
    print("  1. Go to: https://github.com/new")
    print(f"  2. Repository name: {REPO_NAME}")
    print(f"  3. Description: {DESCRIPTION}")
    print("  4. Choose public/private")
    print("  5. Don't initialize with README")
    print("  6. Click 'Create repository'")
    print("  7. Then run:")
    print("     git remote add origin https://github.com/YOUR_USERNAME/" + REPO_NAME + ".git")
    print("     git branch -M main")
    print("     git push -u origin main")
    print("\nOption 3: Use GitHub API Token")
    print("  1. Get token from: https://github.com/settings/tokens")
    print("  2. Create token with 'repo' scope")
    print("  3. Export: export GITHUB_TOKEN=your_token_here")
    print("  4. Run: python3 create_github_repo.py")

if __name__ == '__main__':
    main()

