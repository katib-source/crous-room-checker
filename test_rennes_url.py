#!/usr/bin/env python3
"""
Quick test of the Rennes-specific CROUS URL
"""

import requests
from bs4 import BeautifulSoup

def test_rennes_url():
    # Original URL (all accommodations)
    original_url = "https://trouverunlogement.lescrous.fr/tools/41/search"
    
    # Rennes-specific URL with geographic bounds
    rennes_url = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=-1.7525876_48.1549705_-1.6244045_48.0769155"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print("🧪 Testing CROUS URLs...")
    print("=" * 60)
    
    # Test original URL
    print("📍 Testing original URL (all France):")
    try:
        r1 = requests.get(original_url, headers=session.headers)
        soup1 = BeautifulSoup(r1.content, 'html.parser')
        text1 = soup1.get_text().lower()
        
        print(f"   Status: {r1.status_code}")
        print(f"   Content length: {len(r1.content)} bytes")
        print(f"   Contains 'rennes': {'rennes' in text1}")
        print(f"   Contains 'brive': {'brive' in text1}")
        print(f"   Contains 'tulle': {'tulle' in text1}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test Rennes-specific URL
    print("📍 Testing Rennes-specific URL:")
    try:
        r2 = requests.get(rennes_url, headers=session.headers)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        text2 = soup2.get_text().lower()
        
        print(f"   Status: {r2.status_code}")
        print(f"   Content length: {len(r2.content)} bytes")
        print(f"   Contains 'rennes': {'rennes' in text2}")
        print(f"   Contains 'brive': {'brive' in text2}")
        print(f"   Contains 'tulle': {'tulle' in text2}")
        
        # Count accommodation mentions
        import re
        prices = re.findall(r'\d{2,4}\s*€', text2)
        print(f"   Price mentions found: {len(prices)}")
        
        if len(prices) > 0:
            print(f"   Sample prices: {prices[:5]}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_rennes_url()
    input("Press Enter to exit...")
