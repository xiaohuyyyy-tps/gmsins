#!/usr/bin/env python3
"""
GitHub Push Script for GMS Instagram Stories
Pushes webpage directory content to GitHub repository
"""

import os
import subprocess
import sys
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/xiaohuyyyy-tps/gmsins.git"
WEBPAGE_DIR = Path(__file__).parent
TARGET_DIR = WEBPAGE_DIR

def run_command(cmd, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        print(f"✅ {cmd}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {cmd}")
        print(f"Error: {e.stderr}")
        return False

def setup_git_repo():
    """Initialize git repository if not exists"""
    git_dir = TARGET_DIR / ".git"
    
    if not git_dir.exists():
        print("🔧 Initializing git repository...")
        if not run_command("git init", cwd=str(TARGET_DIR)):
            return False
    else:
        print("✅ Git repository already exists")
    
    return True

def configure_remote():
    """Configure remote repository"""
    print("🔗 Configuring remote repository...")
    
    # Remove existing remote if any
    run_command("git remote remove origin", cwd=str(TARGET_DIR))
    
    # Add new remote
    if not run_command(f"git remote add origin {REPO_URL}", cwd=str(TARGET_DIR)):
        return False
    
    return True

def stage_and_commit():
    """Stage all files and commit"""
    print("📦 Staging files...")
    
    # Add all files
    if not run_command("git add .", cwd=str(TARGET_DIR)):
        return False
    
    # Check if there are changes to commit
    result = subprocess.run(
        "git status --porcelain", 
        shell=True, 
        cwd=str(TARGET_DIR), 
        capture_output=True, 
        text=True
    )
    
    if not result.stdout.strip():
        print("ℹ️ No changes to commit")
        return True
    
    # Commit changes
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Update Instagram story screenshots - {timestamp}"
    
    print(f"📝 Committing changes: {commit_msg}")
    if not run_command(f'git commit -m "{commit_msg}"', cwd=str(TARGET_DIR)):
        return False
    
    return True

def push_to_github():
    """Push to GitHub repository"""
    print("🚀 Pushing to GitHub...")
    
    # Try pushing to main branch first
    if run_command("git push -u origin main", cwd=str(TARGET_DIR)):
        return True
    
    # Try master branch if main fails
    if run_command("git push -u origin master", cwd=str(TARGET_DIR)):
        return True
    
    return False

def get_credentials():
    """Get GitHub credentials from user"""
    print("\n🔐 GitHub Credentials Required")
    print("Repository: https://github.com/xiaohuyyyy-tps/gmsins.git")
    print("-" * 50)
    
    username = input("GitHub username: ").strip()
    password = input("GitHub password/token: ").strip()
    
    return username, password

def setup_credentials():
    """Setup Git credentials for this session"""
    username, password = get_credentials()
    
    # Configure git credentials
    if not run_command(f'git config user.name "{username}"', cwd=str(TARGET_DIR)):
        return False
    
    if not run_command(f'git config user.email "{username}@users.noreply.github.com"', cwd=str(TARGET_DIR)):
        return False
    
    # Setup remote URL with credentials
    cred_url = f"https://{username}:{password}@github.com/xiaohuyyyy-tps/gmsins.git"
    
    print("🔗 Updating remote URL with credentials...")
    if not run_command(f"git remote set-url origin {cred_url}", cwd=str(TARGET_DIR)):
        return False
    
    return True

def main():
    """Main function"""
    print("🐙 GitHub Push Script for GMS Instagram Stories")
    print("=" * 50)
    print(f"Target directory: {TARGET_DIR}")
    print(f"Repository: {REPO_URL}")
    print()
    
    # Change to target directory
    os.chdir(str(TARGET_DIR))
    
    try:
        # Setup git repository
        if not setup_git_repo():
            print("❌ Failed to setup git repository")
            return False
        
        # Configure remote
        if not configure_remote():
            print("❌ Failed to configure remote")
            return False
        
        # Setup credentials
        if not setup_credentials():
            print("❌ Failed to setup credentials")
            return False
        
        # Stage and commit
        if not stage_and_commit():
            print("❌ Failed to stage and commit")
            return False
        
        # Push to GitHub
        if not push_to_github():
            print("❌ Failed to push to GitHub")
            return False
        
        print("\n🎉 Successfully pushed to GitHub!")
        print(f"📂 Repository: {REPO_URL}")
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
