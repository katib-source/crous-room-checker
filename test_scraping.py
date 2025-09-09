#!/usr/bin/env python3
"""
Test script to verify CROUS Rennes website scraping
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def test_crous_scraping():
    """Test the CROUS Rennes website scraping"""
    url = "https://trouverunlogement.lescrous.fr/tools/41/search"
    
    print("🧪 Testing CROUS Rennes website scraping...")
    print(f"🌐 URL: {url}")
    print("=" * 60)
    
    try:
        # Create session with proper headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Get the webpage
        print("📡 Fetching webpage...")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        print(f"✅ Response status: {response.status_code}")
        print(f"📄 Content type: {response.headers.get('content-type', 'Unknown')}")
        print(f"📏 Content length: {len(response.content)} bytes")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get page title
        title = soup.title.string.strip() if soup.title else "No title"
        print(f"📝 Page title: {title}")
        
        # Get page text
        page_text = soup.get_text()
        print(f"📏 Page text length: {len(page_text)} characters")
        
        print("\n" + "=" * 60)
        print("🔍 Analyzing page structure...")
        
        # Look for potential room containers
        potential_containers = []
        
        # Check for common CROUS selectors
        selectors_to_check = [
            ('div[class*="logement"]', 'Logement divs'),
            ('div[class*="accommodation"]', 'Accommodation divs'),
            ('div[class*="result"]', 'Result divs'),
            ('article', 'Article elements'),
            ('tr[class*="logement"]', 'Logement table rows'),
            ('li[class*="logement"]', 'Logement list items'),
            ('div[class*="residence"]', 'Residence divs'),
            ('div[class*="housing"]', 'Housing divs')
        ]
        
        for selector, description in selectors_to_check:
            elements = soup.select(selector)
            if elements:
                print(f"📦 Found {len(elements)} {description}")
                potential_containers.extend(elements)
        
        # If no specific containers found, look for elements with housing-related text
        if not potential_containers:
            print("🔍 No specific containers found, searching for elements with housing text...")
            all_divs = soup.find_all(['div', 'article', 'section'])
            
            for div in all_divs:
                text = div.get_text(strip=True).lower()
                if any(keyword in text for keyword in ['€', 'euro', 'logement', 'studio', 'chambre']):
                    if len(text) > 50:  # Only consider substantial content
                        potential_containers.append(div)
        
        print(f"📦 Total potential room containers: {len(potential_containers)}")
        
        # Analyze potential rooms
        rooms_found = []
        
        for i, container in enumerate(potential_containers[:10]):  # Limit to first 10 for testing
            text = container.get_text(strip=True)
            
            # Skip very short or empty containers
            if len(text) < 20:
                continue
                
            # Skip navigation/menu items
            if any(skip in text.lower() for skip in ['navigation', 'menu', 'header', 'footer']):
                continue
            
            # Look for price
            price_patterns = [
                r'(\d{2,4})\s*€',
                r'(\d{2,4})\s*euros?',
                r'€\s*(\d{2,4})'
            ]
            
            price_found = None
            for pattern in price_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    price_found = match.group(1)
                    break
            
            if price_found:
                # This looks like a room listing
                print(f"\n🏠 Potential room {len(rooms_found) + 1}:")
                print(f"   💰 Price: {price_found}€")
                print(f"   📝 Text preview: {text[:100]}...")
                
                rooms_found.append({
                    'price': price_found,
                    'text': text,
                    'element_type': container.name
                })
        
        print("\n" + "=" * 60)
        print("📊 Summary:")
        print(f"✅ Successfully accessed CROUS website")
        print(f"🏠 Found {len(rooms_found)} potential room listings")
        
        if rooms_found:
            print("🎉 Rooms detected! The scraper should work.")
        else:
            print("⚠️  No rooms found. This could mean:")
            print("   - No rooms are currently available")
            print("   - The website structure has changed")
            print("   - Additional parameters are needed for the search")
        
        # Check for "no results" messages
        no_results_indicators = [
            'aucun résultat', 'no results', 'pas de logement', 'aucun logement',
            'recherche vide', 'aucune offre'
        ]
        
        page_text_lower = page_text.lower()
        for indicator in no_results_indicators:
            if indicator in page_text_lower:
                print(f"📢 Found 'no results' message: '{indicator}'")
                break
        
        return len(rooms_found) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_crous_scraping()
    
    if success:
        print("\n🎉 Test successful! Your CROUS scraper should work.")
        print("💡 You can now run: python crous-checker.py")
    else:
        print("\n⚠️  Test completed but no rooms found.")
        print("💡 This is normal if no rooms are currently available.")
    
    input("\nPress Enter to exit...")
