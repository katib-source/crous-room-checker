"""
CROUS Room Availability Checker with Telegram Notifications

This script checks for available CROUS rooms and sends Telegram notifications
when rooms become available.

Author: GitHub Copilot
Date: September 2025
"""

import requests
import time
import random
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crous_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Handle Telegram bot notifications"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message: str) -> bool:
        """Send a message via Telegram bot"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Telegram notification sent successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
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
        
        # CROUS URL for Nice area with geographic bounds
        self.crous_url = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=7.1819535_43.7607635_7.323912_43.6454189"
        
        # Track previously found rooms to avoid duplicate notifications
        self.previous_rooms = set()
    
    def check_availability_simulation(self) -> Dict[str, Any]:
        """
        Simulate CROUS room availability check
        Replace this with actual web scraping when you have the real URL
        """
        # Simulate random availability (30% chance of finding rooms)
        if random.random() < 0.3:
            num_rooms = random.randint(1, 5)
            rooms = []
            
            for i in range(num_rooms):
                room = {
                    'id': f"ROOM_{random.randint(1000, 9999)}",
                    'type': random.choice(['Studio', 'T1', 'T2', 'Chambre']),
                    'location': random.choice(['Paris 13e', 'Paris 5e', 'Créteil', 'Antony']),
                    'rent': f"{random.randint(300, 600)}€",
                    'available_date': '2025-09-15'
                }
                rooms.append(room)
            
            return {
                'available': True,
                'rooms': rooms,
                'total_count': len(rooms)
            }
        else:
            return {
                'available': False,
                'rooms': [],
                'total_count': 0
            }
    
    def check_availability_real(self) -> Dict[str, Any]:
        """
        Real CROUS website scraping for Nice accommodation
        Scrapes https://trouverunlogement.lescrous.fr/tools/41/search
        """
        try:
            logger.info("Checking CROUS Nice website...")
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
            # Check for common selectors used by CROUS websites
            
            # Method 1: Look for accommodation cards/items
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
                    
                    # Look for price indicators (rooms should have prices)
                    price_match = None
                    price_patterns = [
                        r'(\d{2,4})\s*€',  # Price in euros
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
                    
                    # Create a unique identifier based on price and location text
                    unique_id = f"{price_match}_{hash(room_text[:100]) % 10000}"
                    
                    # Skip if we've already seen this room
                    if unique_id in room_ids_seen:
                        continue
                    
                    room_ids_seen.add(unique_id)
                    
                    # Extract location (look for common location indicators)
                    location = 'Rennes'  # Default to Rennes
                    
                    # Look for specific residence names or addresses
                    residence_patterns = [
                        r'(résidence[^0-9€\n]+)',
                        r'(campus[^0-9€\n]+)',
                        r'(\d+\s+[^0-9€\n]{10,50})',  # Address pattern
                        r'([A-Z][a-z]+\s+[A-Z][a-z]+)'  # City names
                    ]
                    
                    for pattern in residence_patterns:
                        location_match = re.search(pattern, room_text, re.IGNORECASE)
                        if location_match:
                            potential_location = location_match.group(1).strip()
                            if len(potential_location) > 5 and '€' not in potential_location:
                                location = potential_location[:50]  # Limit length
                                break
                    
                    # Extract room type
                    room_type = 'Logement'  # Default
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
    
    def check_and_notify(self, use_simulation: bool = True) -> None:
        """Check for room availability and send notifications if found"""
        try:
            logger.info("Checking CROUS room availability...")
            
            # Choose between simulation and real checking
            if use_simulation:
                result = self.check_availability_simulation()
            else:
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
                print("No rooms yet")
                logger.info("No rooms available")
                
        except Exception as e:
            logger.error(f"Error during availability check: {e}")

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json file"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("config.json not found. Please create it with your Telegram credentials.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error reading config.json: {e}")
        return {}

def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
        "telegram": {
            "bot_token": "YOUR_BOT_TOKEN_HERE",
            "chat_id": "YOUR_CHAT_ID_HERE"
        },
        "settings": {
            "check_interval_minutes": 5,
            "use_simulation": True,
            "log_level": "INFO"
        }
    }
    
    with open('config_sample.json', 'w') as f:
        json.dump(sample_config, f, indent=4)
    
    print("Sample configuration created as 'config_sample.json'")
    print("Please copy it to 'config.json' and fill in your credentials.")

def main():
    """Main function to run the CROUS checker"""
    print("🏠 CROUS Room Availability Checker Starting...")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    if not config:
        print("Creating sample configuration file...")
        create_sample_config()
        return
    
    # Validate required configuration
    telegram_config = config.get('telegram', {})
    bot_token = telegram_config.get('bot_token')
    chat_id = telegram_config.get('chat_id')
    
    if not bot_token or not chat_id or bot_token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please configure your Telegram credentials in config.json")
        print("See setup instructions in the comments above.")
        return
    
    # Initialize components
    telegram_bot = TelegramBot(bot_token, chat_id)
    checker = CrousChecker(telegram_bot)
    
    # Get settings
    settings = config.get('settings', {})
    check_interval = settings.get('check_interval_minutes', 5)
    use_simulation = settings.get('use_simulation', True)
    
    print(f"✅ Bot initialized successfully!")
    print(f"⏰ Check interval: {check_interval} minutes")
    print(f"🎮 Simulation mode: {'ON' if use_simulation else 'OFF'}")
    print("=" * 50)
    
    # Send startup notification
    startup_message = f"""
🤖 <b>CROUS Checker Started!</b>

⏰ Check interval: {check_interval} minutes
🎮 Mode: {'Simulation' if use_simulation else 'Real checking'}
📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

I'll notify you when rooms become available! 🏠
    """
    telegram_bot.send_message(startup_message.strip())
    
    try:
        while True:
            checker.check_and_notify(use_simulation=use_simulation)
            
            # Wait for the specified interval
            logger.info(f"Waiting {check_interval} minutes before next check...")
            time.sleep(check_interval * 60)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping CROUS checker...")
        logger.info("CROUS checker stopped by user")
        
        # Send shutdown notification
        shutdown_message = f"""
🛑 <b>CROUS Checker Stopped</b>

Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Thank you for using the CROUS room checker! 👋
        """
        telegram_bot.send_message(shutdown_message.strip())
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        error_message = f"❌ <b>CROUS Checker Error</b>\n\nError: {str(e)}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        telegram_bot.send_message(error_message)

if __name__ == "__main__":
    main()