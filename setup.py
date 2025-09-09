#!/usr/bin/env python3
"""
Setup script for CROUS Room Checker
"""

import subprocess
import sys
import os
import shutil

def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_config():
    """Create configuration file if it doesn't exist"""
    print("Creating configuration file...")
    
    if os.path.exists("config.json"):
        print("✅ Configuration file already exists.")
        return True
    
    try:
        shutil.copy("config_sample.json", "config.json")
        print("✅ Configuration file created as config.json")
        print("📝 Please edit config.json with your Telegram credentials before running the script.")
        return True
    except Exception as e:
        print(f"❌ Error creating configuration file: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("🏠 CROUS Room Checker - Setup Script")
    print("=" * 50)
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed during dependency installation.")
        return False
    
    print()
    
    # Create configuration
    if not create_config():
        print("Setup failed during configuration creation.")
        return False
    
    print()
    print("=" * 50)
    print("🎉 Setup completed!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Edit config.json with your Telegram bot token and chat ID")
    print("2. Run: python crous-checker.py")
    print()
    print("For detailed instructions, see README.md")
    print()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during setup: {e}")
    
    input("Press Enter to exit...")
