#!/usr/bin/env python3
"""
CROUS Room Availability Checker - Cloud Version for Render
Modified for cloud deployment with environment variables
"""

import requests
import time
import random
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json

# Configure logging for cloud environment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only console logging for cloud
    ]
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Handle Telegram bot notifications"""
    
    def __init__(self, bot_token: str, chat_ids: list):
        self.bot_token = bot_token
        self.chat_ids = chat_ids if isinstance(chat_ids, list) else [chat_ids]
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message: str) -> bool:
        """Send a message to all configured chat IDs"""
        success_count = 0
        
        for chat_id in self.chat_ids:
            try:
                url = f"{self.base_url}/sendMessage"
                payload = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                
                logger.info(f"Telegram notification sent successfully to {chat_id}")
                success_count += 1
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to send Telegram message to {chat_id}: {e}")
        
        if success_count > 0:
            logger.info(f"Message sent to {success_count}/{len(self.chat_ids)} recipients")
            return True
        else:
            logger.error("Failed to send message to any recipient")
            return False

class CrousChecker:
    """CROUS room availability checker"""
    
    def __init__(self, telegram_bot: TelegramBot):
        self.telegram_bot = telegram_bot
        self.session = requests.Session()
        # Set a realistic user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # CROUS URL for Rennes area with geographic bounds
        self.crous_url = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=-1.7525876_48.1549705_-1.6244045_48.0769155"
        
        # Track previously found rooms to avoid duplicate notifications
        self.previous_rooms = set()
    
    def check_availability_real(self) -> Dict[str, Any]:
        """
        Real CROUS website scraping for Rennes accommodation
        """
        try:
            logger.info("Checking CROUS Rennes website...")
            response = self.session.get(self.crous_url, timeout=15)
            response.raise_for_status()
            
            logger.info(f"Response received: {len(response.content)} bytes")
            
            # Parse with BeautifulSoup
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Log page info for debugging
            page_text = soup.get_text()
            logger.info(f"Page text length: {len(page_text)} characters")
            
            # Check if this looks like a "no results" page for Rennes
            if len(page_text) < 1000:  # Very short page might indicate no results
                logger.info("Very short page detected - might be no results for Rennes area")
            
            rooms = []
            
            # Look for room listings - CROUS websites typically use specific patterns
            room_elements = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['logement', 'accommodation', 'room', 'residence', 'housing']
            ))
            
            # Method 2: Look for table rows with accommodation data
            if not room_elements:
                room_elements = soup.find_all('tr', class_=lambda x: x and any(
                    keyword in x.lower() for keyword in ['logement', 'result', 'row']
                ))
            
            # Method 3: Look for list items
            if not room_elements:
                room_elements = soup.find_all('li', class_=lambda x: x and any(
                    keyword in x.lower() for keyword in ['logement', 'accommodation', 'result']
                ))
            
            # Method 4: Check for results container and extract data
            results_container = soup.find(['div', 'section'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['results', 'resultats', 'listings', 'accommodations']
            ))
            
            if results_container and not room_elements:
                room_elements = results_container.find_all(['div', 'article', 'li'])
            
            logger.info(f"Found {len(room_elements)} potential room elements")
            
            # Parse each room element
            room_ids_seen = set()  # Track unique rooms to avoid duplicates
            
            for i, room_elem in enumerate(room_elements):
                try:
                    room_text = room_elem.get_text(strip=True)
                    
                    # Skip empty or very short elements
                    if len(room_text) < 20:
                        continue
                    
                    # Skip navigation, menu, or header elements
                    if any(skip_word in room_text.lower() for skip_word in [
                        'navigation', 'menu', 'header', 'footer', 'cookies', 'rgpd',
                        'filtrer', 'recherche', 'tri', 'page', 'résultat'
                    ]):
                        continue
                    
                    # Look for price indicators
                    price_match = None
                    price_patterns = [
                        r'(\d{2,4})\s*€',
                        r'(\d{2,4})\s*euros?',
                        r'€\s*(\d{2,4})',
                        r'prix.*?(\d{2,4})',
                        r'loyer.*?(\d{2,4})'
                    ]
                    
                    import re
                    for pattern in price_patterns:
                        match = re.search(pattern, room_text, re.IGNORECASE)
                        if match:
                            price_match = match.group(1)
                            break
                    
                    # If no price found, this might not be a room listing
                    if not price_match:
                        continue
                    
                    # Create a unique identifier
                    unique_id = f"{price_match}_{hash(room_text[:100]) % 10000}"
                    
                    # Skip if we've already seen this room
                    if unique_id in room_ids_seen:
                        continue
                    
                    room_ids_seen.add(unique_id)
                    
                    # Extract location
                    location = 'Rennes'
                    residence_patterns = [
                        r'(résidence[^0-9€\n]+)',
                        r'(campus[^0-9€\n]+)',
                        r'(\d+\s+[^0-9€\n]{10,50})',
                        r'([A-Z][a-z]+\s+[A-Z][a-z]+)'
                    ]
                    
                    for pattern in residence_patterns:
                        location_match = re.search(pattern, room_text, re.IGNORECASE)
                        if location_match:
                            potential_location = location_match.group(1).strip()
                            if len(potential_location) > 5 and '€' not in potential_location:
                                location = potential_location[:50]
                                break
                    
                    # Extract room type
                    room_type = 'Logement'
                    type_patterns = [
                        r'(studio)', 
                        r'(t[1-9]|type\s*[1-9])',
                        r'(chambre)',
                        r'(appartement)',
                        r'(\d+\s*pièces?)',
                        r'(\d+\s*m²)'
                    ]
                    for pattern in type_patterns:
                        type_match = re.search(pattern, room_text, re.IGNORECASE)
                        if type_match:
                            room_type = type_match.group(1).title()
                            break
                    
                    # Create room info
                    room_info = {
                        'id': unique_id,
                        'type': room_type,
                        'location': location,
                        'rent': f"{price_match}€",
                        'available_date': datetime.now().strftime('%Y-%m-%d'),
                        'url': self.crous_url
                    }
                    
                    rooms.append(room_info)
                    logger.info(f"Found unique room: {room_type} in {location} for {price_match}€")
                    
                except Exception as e:
                    logger.warning(f"Error parsing room element {i}: {e}")
                    continue
            
            # Check for "no results" messages
            no_results_indicators = [
                'aucun résultat', 'no results', 'pas de logement', 'aucun logement',
                'recherche vide', 'aucune offre'
            ]
            
            page_text = soup.get_text().lower()
            has_no_results = any(indicator in page_text for indicator in no_results_indicators)
            
            if rooms:
                logger.info(f"Successfully found {len(rooms)} rooms on CROUS website")
                return {
                    'available': True,
                    'rooms': rooms,
                    'total_count': len(rooms)
                }
            elif has_no_results:
                logger.info("CROUS website explicitly shows no results")
                return {
                    'available': False,
                    'rooms': [],
                    'total_count': 0
                }
            else:
                logger.warning("Could not find room listings or no results message")
                return {
                    'available': False,
                    'rooms': [],
                    'total_count': 0,
                    'note': 'Website structure may have changed'
                }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking CROUS website: {e}")
            return {
                'available': False,
                'rooms': [],
                'total_count': 0,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error parsing CROUS website: {e}")
            return {
                'available': False,
                'rooms': [],
                'total_count': 0,
                'error': str(e)
            }
    
    def format_room_message(self, rooms: list) -> str:
        """Format room information for Telegram message"""
        
        # Limit the number of rooms in a single message to avoid Telegram length limits
        max_rooms_per_message = 5
        limited_rooms = rooms[:max_rooms_per_message]
        
        message = f"🏠 <b>CROUS Rennes Area - {len(rooms)} Rooms Available!</b>\n\n"
        
        for i, room in enumerate(limited_rooms, 1):
            message += f"<b>Room {i}:</b>\n"
            message += f"📍 {room['location']}\n"
            message += f"🏡 {room['type']}\n"
            message += f"💰 {room['rent']}\n"
            message += f"🆔 {room['id'][:20]}...\n\n"
        
        if len(rooms) > max_rooms_per_message:
            message += f"... and {len(rooms) - max_rooms_per_message} more rooms!\n\n"
        
        message += f"📊 Total: {len(rooms)} rooms found\n"
        message += f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
        message += f"🔗 <a href='https://trouverunlogement.lescrous.fr/tools/41/search'>View all on CROUS</a>"
        
        return message
    
    def check_and_notify(self) -> None:
        """Check for room availability and send notifications if found"""
        try:
            logger.info("Checking CROUS room availability...")
            
            result = self.check_availability_real()
            
            if result['available'] and result['rooms']:
                # Check for new rooms to avoid duplicate notifications
                current_room_ids = {room['id'] for room in result['rooms']}
                new_rooms = [room for room in result['rooms'] 
                           if room['id'] not in self.previous_rooms]
                
                if new_rooms:
                    message = self.format_room_message(new_rooms)
                    
                    # Send Telegram notification
                    success = self.telegram_bot.send_message(message)
                    
                    if success:
                        logger.info(f"Found {len(new_rooms)} new room(s), notification sent!")
                        # Update previous rooms set
                        self.previous_rooms.update(current_room_ids)
                    else:
                        logger.error("Failed to send notification")
                else:
                    logger.info(f"Found {len(result['rooms'])} room(s), but all were already notified")
            else:
                logger.info("No rooms available")
                
        except Exception as e:
            logger.error(f"Error during availability check: {e}")

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables or config file"""
    config = {}
    
    # Try to load from environment variables first (for cloud deployment)
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_ids_env = os.getenv('TELEGRAM_CHAT_IDS')  # Comma-separated list
    chat_id_single = os.getenv('TELEGRAM_CHAT_ID')  # Single chat ID (backward compatibility)
    check_interval = os.getenv('CHECK_INTERVAL_MINUTES', '5')
    
    # Parse chat IDs
    chat_ids = []
    if chat_ids_env:
        # Multiple chat IDs from TELEGRAM_CHAT_IDS (comma-separated)
        chat_ids = [id.strip() for id in chat_ids_env.split(',') if id.strip()]
    elif chat_id_single:
        # Single chat ID from TELEGRAM_CHAT_ID (backward compatibility)
        chat_ids = [chat_id_single]
    
    if bot_token and chat_ids:
        logger.info(f"Loading configuration from environment variables for {len(chat_ids)} recipient(s)")
        config = {
            "telegram": {
                "bot_token": bot_token,
                "chat_ids": chat_ids
            },
            "settings": {
                "check_interval_minutes": int(check_interval),
                "use_simulation": False,
                "log_level": "INFO"
            }
        }
    else:
        # Fallback to config.json for local development
        try:
            logger.info("Loading configuration from config.json")
            with open('config.json', 'r') as f:
                config = json.load(f)
                
            # Convert single chat_id to list for backward compatibility
            telegram_config = config.get('telegram', {})
            if 'chat_id' in telegram_config and 'chat_ids' not in telegram_config:
                telegram_config['chat_ids'] = [telegram_config['chat_id']]
            elif 'chat_ids' in telegram_config:
                # Ensure chat_ids is a list
                if isinstance(telegram_config['chat_ids'], str):
                    telegram_config['chat_ids'] = [telegram_config['chat_ids']]
                    
        except FileNotFoundError:
            logger.error("No configuration found. Set environment variables or create config.json")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error reading config.json: {e}")
            return {}
    
    return config

def main():
    """Main function to run the CROUS checker"""
    logger.info("🏠 CROUS Room Availability Checker Starting...")
    logger.info("=" * 50)
    
    # Load configuration
    config = load_config()
    
    if not config:
        logger.error("❌ No valid configuration found")
        return
    
    # Validate required configuration
    telegram_config = config.get('telegram', {})
    bot_token = telegram_config.get('bot_token')
    chat_ids = telegram_config.get('chat_ids', [])
    
    # Backward compatibility with single chat_id
    if not chat_ids and telegram_config.get('chat_id'):
        chat_ids = [telegram_config.get('chat_id')]
    
    if not bot_token or not chat_ids:
        logger.error("❌ Missing Telegram credentials")
        return
    
    # Initialize components
    telegram_bot = TelegramBot(bot_token, chat_ids)
    checker = CrousChecker(telegram_bot)
    
    # Get settings
    settings = config.get('settings', {})
    check_interval = settings.get('check_interval_minutes', 5)
    
    logger.info(f"✅ Bot initialized successfully!")
    logger.info(f"👥 Recipients: {len(chat_ids)} user(s)")
    logger.info(f"⏰ Check interval: {check_interval} minutes")
    logger.info(f"🎮 Simulation mode: OFF")
    logger.info("=" * 50)
    
    # Send startup notification
    startup_message = f"""
🤖 <b>CROUS Checker Started on Render!</b>

👥 Notifying: {len(chat_ids)} user(s)
⏰ Check interval: {check_interval} minutes
🎯 Monitoring: Rennes area only
📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
☁️ Running on: Render Cloud

I'll notify you when rooms become available! 🏠
    """
    telegram_bot.send_message(startup_message.strip())
    
    try:
        while True:
            checker.check_and_notify()
            
            # Wait for the specified interval
            logger.info(f"Waiting {check_interval} minutes before next check...")
            time.sleep(check_interval * 60)
            
    except KeyboardInterrupt:
        logger.info("🛑 Stopping CROUS checker...")
        
        # Send shutdown notification
        shutdown_message = f"""
🛑 <b>CROUS Checker Stopped</b>

Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Service has been terminated. 👋
        """
        telegram_bot.send_message(shutdown_message.strip())
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        error_message = f"❌ <b>CROUS Checker Error</b>\n\nError: {str(e)}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        telegram_bot.send_message(error_message)

if __name__ == "__main__":
    main()
