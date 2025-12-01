#!/usr/bin/env python3
"""
Test script for new welcome animations
"""

import os
import time

def test_animation_files():
    """Test if animation files exist"""
    print("🎬 Testing Animation Files...")
    
    files_to_check = [
        "Frontend/index.html",
        "Frontend/settings.css",
        "Frontend/controller.js"
    ]
    
    success = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} missing")
            success = False
    
    return success

def test_html_elements():
    """Test if HTML contains new animation elements"""
    print("🔍 Testing HTML Elements...")
    
    try:
        with open("Frontend/index.html", 'r') as f:
            html_content = f.read()
        
        elements_to_check = [
            'id="WelcomeAnimation"',
            'id="SystemReady"',
            'class="welcome-container"',
            'class="ai-icon-container"',
            'class="success-container"',
            'class="checkmark-circle"'
        ]
        
        success = True
        for element in elements_to_check:
            if element in html_content:
                print(f"   ✅ {element} found")
            else:
                print(f"   ❌ {element} missing")
                success = False
        
        return success
    
    except Exception as e:
        print(f"   ❌ Error reading HTML: {e}")
        return False

def test_css_animations():
    """Test if CSS contains animation styles"""
    print("🎨 Testing CSS Animations...")
    
    try:
        with open("Frontend/settings.css", 'r') as f:
            css_content = f.read()
        
        animations_to_check = [
            '@keyframes fadeInUp',
            '@keyframes bounceIn',
            '@keyframes pulse',
            '@keyframes dotPulse',
            '@keyframes checkmarkDraw',
            '.welcome-container',
            '.ai-core',
            '.checkmark-circle'
        ]
        
        success = True
        for animation in animations_to_check:
            if animation in css_content:
                print(f"   ✅ {animation} found")
            else:
                print(f"   ❌ {animation} missing")
                success = False
        
        return success
    
    except Exception as e:
        print(f"   ❌ Error reading CSS: {e}")
        return False

def test_js_functions():
    """Test if JavaScript contains new functions"""
    print("⚙️ Testing JavaScript Functions...")
    
    try:
        with open("Frontend/controller.js", 'r') as f:
            js_content = f.read()
        
        functions_to_check = [
            'showWelcomeAnimation',
            'showSystemReady',
            'hideWelcomeAnimations',
            'eel.expose(showWelcomeAnimation)',
            'eel.expose(showSystemReady)',
            'eel.expose(hideWelcomeAnimations)'
        ]
        
        success = True
        for function in functions_to_check:
            if function in js_content:
                print(f"   ✅ {function} found")
            else:
                print(f"   ❌ {function} missing")
                success = False
        
        return success
    
    except Exception as e:
        print(f"   ❌ Error reading JavaScript: {e}")
        return False

def test_main_py_integration():
    """Test if main.py uses new animations"""
    print("🐍 Testing Python Integration...")
    
    try:
        with open("main.py", 'r') as f:
            py_content = f.read()
        
        integrations_to_check = [
            'eel.showWelcomeAnimation()',
            'eel.showSystemReady()',
            'eel.hideWelcomeAnimations()',
            'Show welcome animation while speaking',
            'Show system ready animation'
        ]
        
        success = True
        for integration in integrations_to_check:
            if integration in py_content:
                print(f"   ✅ {integration} found")
            else:
                print(f"   ❌ {integration} missing")
                success = False
        
        return success
    
    except Exception as e:
        print(f"   ❌ Error reading main.py: {e}")
        return False

def main():
    """Run all animation tests"""
    print("🎬 Jarvis Welcome Animation Test Suite")
    print("=" * 45)
    
    tests = [
        ("Animation Files", test_animation_files),
        ("HTML Elements", test_html_elements),
        ("CSS Animations", test_css_animations),
        ("JavaScript Functions", test_js_functions),
        ("Python Integration", test_main_py_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 45)
    print("📊 ANIMATION TEST RESULTS")
    print("=" * 45)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nOverall Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL ANIMATION TESTS PASSED!")
        print("Welcome animations are ready!")
    elif passed >= total * 0.8:
        print("\n✅ ANIMATIONS MOSTLY WORKING!")
        print("Minor issues detected but animations should work.")
    else:
        print("\n⚠️  ANIMATION ISSUES DETECTED!")
        print("Please fix the failed tests.")
    
    print("\n🎬 New Animation Features:")
    print("- Beautiful welcome screen with AI robot icon")
    print("- Pulsing rings and floating animations")
    print("- Feature icons with hover effects")
    print("- Loading dots animation")
    print("- System ready checkmark animation")
    print("- Smooth transitions between screens")
    print("\n🚀 Now when Jarvis starts, you'll see:")
    print("1. Welcome animation with 'Hello, Welcome Sir'")
    print("2. System ready animation with 'How can I Help You'")
    print("3. Smooth transition to main interface")

if __name__ == "__main__":
    main()
