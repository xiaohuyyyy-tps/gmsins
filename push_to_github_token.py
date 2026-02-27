#!/usr/bin/env python3
"""
GitHub Push Script for GMS Instagram Stories
Pushes webpage directory content to GitHub repository using Personal Access Token
"""

import os
import subprocess
import sys
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/xiaohuyyyy-tps/gmsins.git"
WEBPAGE_DIR = Path(__file__).parent
TARGET_DIR = WEBPAGE_DIR
# Store token in parent directory to avoid pushing it
TOKEN_FILE = WEBPAGE_DIR.parent / ".github_token"

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
        print("[OK] ", cmd)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("[ERROR] ", cmd)
        print(f"Error: {e.stderr}")
        return False

def save_token(token):
    """Save token to file"""
    try:
        with open(TOKEN_FILE, 'w') as f:
            f.write(token.strip())
        # Hide the file on Windows
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(str(TOKEN_FILE), 2)  # FILE_ATTRIBUTE_HIDDEN
        print("[OK] Token saved successfully")
        return True
    except Exception as e:
        print("[ERROR] Failed to save token: {e}")
        return False

def load_token():
    """Load token from file"""
    try:
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'r') as f:
                return f.read().strip()
        return None
    except Exception:
        return None

def get_token():
    """Get GitHub Personal Access Token"""
    # Try to load existing token
    existing_token = load_token()
    if existing_token:
        print("[OK] Found existing token")
        return existing_token
    
    print("\nGitHub Personal Access Token Required")
    print("=" * 50)
    print("To create a Personal Access Token:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Select scopes: repo (Full control of private repositories)")
    print("4. Generate and copy the token")
    print("=" * 50)
    
    token = input("Enter your GitHub Personal Access Token: ").strip()
    
    if not token:
        print("[ERROR] No token provided")
        return None
    
    # Ask if user wants to save the token
    save_choice = input("Save token for future use? (y/n): ").strip().lower()
    if save_choice in ['y', 'yes']:
        if not save_token(token):
            print("Token not saved, will use for this session only")
            print("[WARNING] Token not saved, will use for this session only")
    
    return token

def setup_git_config():
    """Setup basic git configuration"""
    print("[CONFIG] Setting up git configuration...")
    
    # Fixed username
    username = "xiaohuyyyy-tps"
    print(f"[INFO] Using username: {username}")
    
    # Configure git user
    if not run_command(f'git config user.name "{username}"', cwd=str(TARGET_DIR)):
        return False
    
    if not run_command(f'git config user.email "{username}@users.noreply.github.com"', cwd=str(TARGET_DIR)):
        return False
    
    return True

def setup_remote_with_token(token):
    """Configure remote repository with token"""
    print("[CONFIG] Configuring remote repository with token...")
    
    # Remove existing remote if any
    run_command("git remote remove origin", cwd=str(TARGET_DIR))
    
    # Add remote with token
    token_url = f"https://{token}@github.com/xiaohuyyyy-tps/gmsins.git"
    if not run_command(f"git remote add origin {token_url}", cwd=str(TARGET_DIR)):
        return False
    
    return True

def setup_git_repo():
    """Initialize git repository if not exists"""
    git_dir = TARGET_DIR / ".git"
    
    if not git_dir.exists():
        print("[INIT] Initializing git repository...")
        if not run_command("git init", cwd=str(TARGET_DIR)):
            return False
    else:
        print("[OK] Git repository already exists")
    
    return True

def stage_and_commit():
    """Stage all files and commit"""
    print("[STAGE] Staging files...")
    
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
        print("[INFO] No changes to commit")
        return True
    
    # Commit changes
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Update Instagram story screenshots - {timestamp}"
    
    print(f"[COMMIT] Committing changes: {commit_msg}")
    if not run_command(f'git commit -m "{commit_msg}"', cwd=str(TARGET_DIR)):
        return False
    
    return True

def push_to_github():
    """Push to GitHub repository"""
    print("[PUSH] Pushing to GitHub...")
    
    # Try pulling first to handle remote changes
    print("[SYNC] Pulling remote changes first...")
    run_command("git pull origin main --allow-unrelated-histories", cwd=str(TARGET_DIR))
    
    # Try pushing to main branch
    if run_command("git push -u origin main", cwd=str(TARGET_DIR)):
        return True
    
    # Try master branch if main fails
    if run_command("git push -u origin master", cwd=str(TARGET_DIR)):
        return True
    
    return False

def main():
    """Main function"""
    print("GitHub Push Script for GMS Instagram Stories")
    print("=" * 50)
    print(f"Target directory: {TARGET_DIR}")
    print(f"Repository: {REPO_URL}")
    print()
    
    # Change to target directory
    os.chdir(str(TARGET_DIR))
    
    try:
        # Get token
        token = get_token()
        if not token:
            print("[ERROR] Failed to get token")
            return False
        
        # Setup git repository
        if not setup_git_repo():
            print("[ERROR] Failed to setup git repository")
            return False
        
        # Setup git config
        if not setup_git_config():
            print("[ERROR] Failed to setup git configuration")
            return False
        
        # Setup remote with token
        if not setup_remote_with_token(token):
            print("[ERROR] Failed to setup remote")
            return False
        
        # Stage and commit
        if not stage_and_commit():
            print("[ERROR] Failed to stage and commit")
            return False
        
        # Push to GitHub
        if not push_to_github():
            print("[ERROR] Failed to push to GitHub")
            return False
        
        print("\n[SUCCESS] Successfully pushed to GitHub!")
        print(f"Repository: {REPO_URL}")
        return True
        
    except KeyboardInterrupt:
        print("[CANCELLED] Operation cancelled by user")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
