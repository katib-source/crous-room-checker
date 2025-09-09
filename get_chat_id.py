#!/usr/bin/env python3
"""
Quick script to get your Telegram Chat ID
Run this script and then send a message to your bot to get your chat ID
"""

import requests
import json
import time

# Your bot token
BOT_TOKEN = "8465766993:AAGpWR_LPuCFtEq3RdmvO733x3O7bOAwg2A"

def get_chat_id():
    """Get chat ID from recent messages to your bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    print("🤖 Getting your Chat ID...")
    print(f"📱 Go to your bot: https://t.me/KatibCrousBot")
    print("📝 Send any message to your bot (like 'hello')")
    print("⏳ Waiting for your message...")
    print()
    
    # Wait for a message
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get('ok') and data.get('result'):
                for update in data['result']:
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        username = update['message']['chat'].get('username', 'N/A')
                        first_name = update['message']['chat'].get('first_name', 'N/A')
                        
                        print("✅ Found your message!")
                        print(f"🆔 Your Chat ID: {chat_id}")
                        print(f"👤 Name: {first_name}")
                        print(f"📛 Username: @{username}" if username != 'N/A' else "📛 Username: Not set")
                        print()
                        print("🔧 Updating your config.json file...")
                        
                        # Update config.json
                        try:
                            with open('config.json', 'r') as f:
                                config = json.load(f)
                            
                            config['telegram']['chat_id'] = str(chat_id)
                            
                            with open('config.json', 'w') as f:
                                json.dump(config, f, indent=4)
                            
                            print("✅ Config updated successfully!")
                            print("🚀 You can now run: python crous-checker.py")
                            return chat_id
                            
                        except Exception as e:
                            print(f"❌ Error updating config: {e}")
                            print(f"💡 Manually add this Chat ID to config.json: {chat_id}")
                            return chat_id
            
            print("⏳ Still waiting for your message... (send any message to your bot)")
            time.sleep(2)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n⚠️ Cancelled by user")
            return None

if __name__ == "__main__":
    print("=" * 60)
    print("🆔 Telegram Chat ID Finder")
    print("=" * 60)
    
    chat_id = get_chat_id()
    
    if chat_id:
        print()
        print("=" * 60)
        print("🎉 Setup Complete!")
        print("=" * 60)
        print("Next steps:")
        print("1. Run the test: python test_setup.py")
        print("2. Start the checker: python crous-checker.py")
    
    input("\nPress Enter to exit...")
