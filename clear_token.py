#!/usr/bin/env python3
"""
Clear saved GitHub token
"""

from pathlib import Path

TOKEN_FILE = Path(__file__).parent / ".github_token"

if TOKEN_FILE.exists():
    TOKEN_FILE.unlink()
    print("✅ GitHub token cleared successfully")
else:
    print("ℹ️ No saved token found")
