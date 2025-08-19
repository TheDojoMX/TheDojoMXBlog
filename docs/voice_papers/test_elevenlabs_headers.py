#!/usr/bin/env python3
"""Test script to explore ElevenLabs API response headers."""

import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_response_headers():
    """Test ElevenLabs API to see what headers are returned."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment")
        return
    
    client = ElevenLabs(api_key=api_key)
    
    # Test text
    test_text = "Hello, this is a test to explore the response headers."
    
    try:
        # Use with_raw_response to access headers
        with client.text_to_speech.with_raw_response.convert(
            voice_id="sDh3eviBhiuHKi0MjTNq",  # Rachel voice
            text=test_text,
            model_id="eleven_flash_v2_5",
        ) as response:
            # Print all response headers
            print("=== RESPONSE HEADERS ===")
            headers = response._response.headers
            for header, value in headers.items():
                print(f"{header}: {value}")
            
            print(f"\n=== SPECIFIC HEADERS ===")
            print(f"Request ID: {headers.get('request-id', 'NOT FOUND')}")
            print(f"Character Cost: {headers.get('x-character-cost', 'NOT FOUND')}")
            print(f"Credits Used: {headers.get('x-credits-used', 'NOT FOUND')}")
            print(f"Remaining Credits: {headers.get('x-remaining-credits', 'NOT FOUND')}")
            print(f"Character Count: {headers.get('x-character-count', 'NOT FOUND')}")
            
            # Check for any header containing 'credit', 'cost', 'usage', 'quota', 'character'
            print(f"\n=== HEADERS CONTAINING KEYWORDS ===")
            keywords = ['credit', 'cost', 'usage', 'quota', 'character', 'limit', 'rate']
            for header, value in headers.items():
                header_lower = header.lower()
                if any(keyword in header_lower for keyword in keywords):
                    print(f"{header}: {value}")
            
            print(f"\n=== TEXT INFO ===")
            print(f"Text length: {len(test_text)} characters")
            print(f"Estimated cost at 1 credit/char: {len(test_text)} credits")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_response_headers()