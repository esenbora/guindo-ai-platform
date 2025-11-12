#!/usr/bin/env python3
"""
Test script to verify installation and configuration
"""

import os
import sys


def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing package imports...")
    
    required_packages = [
        ('crewai', 'CrewAI'),
        ('langchain_groq', 'LangChain Groq'),
        ('pandas', 'Pandas'),
        ('dotenv', 'Python-dotenv'),
        ('yaml', 'PyYAML'),
    ]
    
    failed = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ✗ {name} - NOT FOUND")
            failed.append(name)
    
    return len(failed) == 0


def test_env_file():
    """Test if .env file exists and has required keys."""
    print("\n🔑 Testing environment configuration...")
    
    if not os.path.exists('.env'):
        print("   ✗ .env file not found")
        print("   → Run: cp .env.example .env")
        return False
    
    print("   ✓ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY')
    serper_key = os.getenv('SERPER_API_KEY')
    
    if not groq_key or groq_key == 'your_groq_api_key_here':
        print("   ✗ GROQ_API_KEY not configured")
        return False
    else:
        print(f"   ✓ GROQ_API_KEY configured ({groq_key[:10]}...)")
    
    if not serper_key or serper_key == 'your_serper_api_key_here':
        print("   ⚠️  SERPER_API_KEY not configured (optional)")
    else:
        print(f"   ✓ SERPER_API_KEY configured ({serper_key[:10]}...)")
    
    return True


def test_directory_structure():
    """Test if all required directories exist."""
    print("\n📁 Testing directory structure...")
    
    required_dirs = ['agents', 'tools', 'config', 'outputs']
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"   ✓ {directory}/")
        else:
            print(f"   ✗ {directory}/ - NOT FOUND")
            all_exist = False
    
    return all_exist


def test_config_files():
    """Test if configuration files exist."""
    print("\n⚙️  Testing configuration files...")
    
    required_files = [
        'config/agents.yaml',
        'config/tasks.yaml',
        'requirements.txt',
        'main.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist


def test_groq_connection():
    """Test Groq API connection."""
    print("\n🌐 Testing Groq API connection...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key or groq_key == 'your_groq_api_key_here':
        print("   ⚠️  Skipping (API key not configured)")
        return True
    
    try:
        from langchain_groq import ChatGroq
        
        llm = ChatGroq(
            model='llama-3.3-70b-versatile',
            groq_api_key=groq_key,
            temperature=0.7
        )
        
        response = llm.invoke("Say 'test successful' if you can read this.")
        print(f"   ✓ Connection successful")
        print(f"   Response: {response.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"   ✗ Connection failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("🚀 Early Retirement Workflow - Setup Test")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment File", test_env_file),
        ("Directory Structure", test_directory_structure),
        ("Configuration Files", test_config_files),
        ("Groq API Connection", test_groq_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to run the workflow.")
        print("   Run: python main.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
