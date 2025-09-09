#!/usr/bin/env python3
"""
Test script for CROUS Room Checker
Run this to verify your setup is working correctly.
"""

import json
import sys
import requests
from datetime import datetime

def test_config():
    """Test if configuration file exists and is valid"""
    print("📋 Testing configuration...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        telegram_config = config.get('telegram', {})
        bot_token = telegram_config.get('bot_token')
        chat_id = telegram_config.get('chat_id')
        
        if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
            print("❌ Bot token not configured in config.json")
            return False
        
        if not chat_id or chat_id == "YOUR_CHAT_ID_HERE":
            print("❌ Chat ID not configured in config.json")
            return False
        
        print("✅ Configuration file is valid")
        return True, config
        
    except FileNotFoundError:
        print("❌ config.json not found. Run setup.py first.")
        return False, None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return False, None

def test_telegram_bot(bot_token, chat_id):
    """Test Telegram bot connectivity"""
    print("🤖 Testing Telegram bot...")
    
    try:
        # Test bot token
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        bot_info = response.json()
        if bot_info.get('ok'):
            bot_name = bot_info['result']['first_name']
            print(f"✅ Bot '{bot_name}' is accessible")
        else:
            print("❌ Invalid bot token")
            return False
        
        # Test sending a message
        test_message = f"🧪 Test message from CROUS Checker\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': test_message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print("✅ Test message sent successfully!")
            print("📱 Check your Telegram to confirm you received the test message.")
            return True
        else:
            print(f"❌ Failed to send message: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are installed"""
    print("📦 Testing dependencies...")
    
    required_modules = ['requests', 'bs4', 'lxml']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} is installed")
        except ImportError:
            print(f"❌ {module} is missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 CROUS Room Checker - Test Script")
    print("=" * 60)
    print()
    
    all_tests_passed = True
    
    # Test dependencies
    if not test_dependencies():
        all_tests_passed = False
    
    print()
    
    # Test configuration
    config_valid, config = test_config()
    if not config_valid:
        all_tests_passed = False
    
    print()
    
    # Test Telegram bot if config is valid
    if config_valid and config:
        telegram_config = config.get('telegram', {})
        bot_token = telegram_config.get('bot_token')
        chat_id = telegram_config.get('chat_id')
        
        if not test_telegram_bot(bot_token, chat_id):
            all_tests_passed = False
    
    print()
    print("=" * 60)
    
    if all_tests_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("🚀 You can now run: python crous-checker.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("📖 Check README.md for detailed setup instructions.")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during testing: {e}")
    
    input("\nPress Enter to exit...")
