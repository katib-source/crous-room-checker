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
        
        # Handle both single chat_id and multiple chat_ids
        chat_ids = telegram_config.get('chat_ids', [])
        chat_id_single = telegram_config.get('chat_id')
        
        if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
            print("❌ Bot token not configured in config.json")
            return False, None
        
        # Check if we have at least one chat ID
        if not chat_ids and not chat_id_single:
            print("❌ No chat IDs configured in config.json")
            return False, None
        
        if chat_ids and any(id == "YOUR_CHAT_ID_HERE" for id in chat_ids):
            print("❌ Default chat ID placeholder found in config.json")
            return False, None
        
        if chat_id_single == "YOUR_CHAT_ID_HERE":
            print("❌ Default chat ID placeholder found in config.json")
            return False, None
        
        # Count total recipients
        total_recipients = len(chat_ids) if chat_ids else (1 if chat_id_single else 0)
        print(f"✅ Configuration file is valid ({total_recipients} recipient(s))")
        return True, config
        
    except FileNotFoundError:
        print("❌ config.json not found. Run setup.py first.")
        return False, None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return False, None

def test_telegram_bot(bot_token, chat_ids):
    """Test Telegram bot connectivity with multiple users"""
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
        
        # Ensure chat_ids is a list
        if isinstance(chat_ids, str):
            chat_ids = [chat_ids]
        
        print(f"🧪 Testing message delivery to {len(chat_ids)} recipient(s)...")
        
        # Test sending messages to all chat IDs
        success_count = 0
        for i, chat_id in enumerate(chat_ids, 1):
            test_message = f"🧪 Test message {i}/{len(chat_ids)} from CROUS Checker\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nRecipient: {chat_id}"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': test_message
            }
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                
                result = response.json()
                if result.get('ok'):
                    print(f"✅ Test message sent successfully to {chat_id}")
                    success_count += 1
                else:
                    print(f"❌ Failed to send message to {chat_id}: {result.get('description', 'Unknown error')}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error sending to {chat_id}: {e}")
        
        if success_count == len(chat_ids):
            print(f"🎉 All {success_count} messages sent successfully!")
            print("📱 Check Telegram to confirm you received the test messages.")
            return True
        elif success_count > 0:
            print(f"⚠️ Partial success: {success_count}/{len(chat_ids)} messages sent")
            print("📱 Check which recipients received messages and verify their chat IDs")
            return True
        else:
            print("❌ Failed to send messages to any recipients")
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
        
        # Handle both single chat_id and multiple chat_ids
        chat_ids = telegram_config.get('chat_ids', [])
        if not chat_ids and telegram_config.get('chat_id'):
            chat_ids = [telegram_config.get('chat_id')]
        
        if not test_telegram_bot(bot_token, chat_ids):
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
