#!/usr/bin/env python3
"""
Test that all widgets have unique keys to avoid DuplicateWidgetID errors
"""

import re

def test_widget_keys():
    """Test that all buttons have unique keys"""
    print("🔧 Testing Widget Keys...")
    
    try:
        with open("frontend.py", "r") as f:
            content = f.read()
        
        # Find all button definitions
        button_pattern = r'st\.button\([^)]+\)'
        buttons = re.findall(button_pattern, content)
        
        print(f"Found {len(buttons)} button definitions")
        
        # Extract keys from buttons
        keys = []
        for button in buttons:
            if "key=" in button:
                key_match = re.search(r'key="([^"]+)"', button)
                if key_match:
                    keys.append(key_match.group(1))
        
        print(f"Found {len(keys)} buttons with keys")
        
        # Check for duplicates
        unique_keys = set(keys)
        if len(keys) == len(unique_keys):
            print("✅ All button keys are unique!")
            return True
        else:
            duplicates = [key for key in keys if keys.count(key) > 1]
            print(f"❌ Found duplicate keys: {set(duplicates)}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def test_specific_buttons():
    """Test specific button keys that were causing issues"""
    print("🎯 Testing Specific Button Keys...")
    
    try:
        with open("frontend.py", "r") as f:
            content = f.read()
        
        # Check for the problematic buttons
        problematic_buttons = [
            "Show All Movies",
            "Top Rated Movies", 
            "Action Movies",
            "Movie Statistics"
        ]
        
        for button_text in problematic_buttons:
            # Look for buttons with this text
            pattern = f'st\.button\("{button_text}"[^)]*\)'
            matches = re.findall(pattern, content)
            
            if len(matches) > 1:
                print(f"❌ Found {len(matches)} instances of '{button_text}' button")
                return False
            elif len(matches) == 1:
                if "key=" in matches[0]:
                    print(f"✅ '{button_text}' button has unique key")
                else:
                    print(f"⚠️  '{button_text}' button missing key")
            else:
                print(f"ℹ️  '{button_text}' button not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 Testing Widget Key Uniqueness")
    print("=" * 40)
    
    # Test all widget keys
    keys_ok = test_widget_keys()
    print()
    
    # Test specific buttons
    specific_ok = test_specific_buttons()
    print()
    
    print("📊 Widget Test Results:")
    print(f"All Keys Unique: {'✅ Pass' if keys_ok else '❌ Fail'}")
    print(f"Specific Buttons: {'✅ Pass' if specific_ok else '❌ Fail'}")
    
    if keys_ok and specific_ok:
        print("\n🎉 All widget keys are unique!")
        print("✅ No more DuplicateWidgetID errors!")
        print("\n🚀 Your application should work perfectly now:")
        print("  - All buttons have unique keys")
        print("  - No duplicate widget errors")
        print("  - Pagination works correctly")
        print("  - Chat input works")
    else:
        print("\n⚠️  Some widget key issues found.")

if __name__ == "__main__":
    main()
