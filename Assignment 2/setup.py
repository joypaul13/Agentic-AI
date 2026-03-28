"""
Quick Start Guide for Autonomous Research Agent
"""
import os
import sys


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'langchain',
        'langchain_community',
        'wikipedia',
        'requests',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_env_file():
    """Check if .env file exists and has required keys"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("   Please copy .env.example to .env and fill in your API keys")
        return False
    
    print("✓ .env file found")
    
    # Check for required keys
    from dotenv import load_dotenv, dotenv_values
    env_vars = dotenv_values(".env")
    
    # Check for at least one LLM API key
    has_api_key = False
    if env_vars.get("OPENAI_API_KEY"):
        print("✓ OpenAI API key found")
        has_api_key = True
    elif env_vars.get("ANTHROPIC_API_KEY"):
        print("✓ Anthropic API key found")
        has_api_key = True
    else:
        print("❌ No LLM API key found (OpenAI or Anthropic)")
        return False
    
    if env_vars.get("SERPAPI_KEY"):
        print("✓ SerpAPI key found (optional)")
    
    return True


def setup_project():
    """Setup project for first use"""
    print("\n" + "="*60)
    print("AUTONOMOUS RESEARCH AGENT - SETUP")
    print("="*60 + "\n")
    
    # Check Python
    print("Checking Python version...")
    if not check_python_version():
        return False
    
    print("\nChecking dependencies...")
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        return False
    
    print("\nChecking environment configuration...")
    if not check_env_file():
        print("\nTo get started:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys to .env")
        print("3. Run this setup again")
        return False
    
    print("\n" + "="*60)
    print("✓ All checks passed! Ready to use.")
    print("="*60)
    print("\nNext steps:")
    print("1. Basic usage:")
    print("   python main.py")
    print("\n2. Research specific topic:")
    print("   python main.py \"Your Topic Here\"")
    print("\n3. Run demos:")
    print("   python demo.py")
    print("\nDocumentation: See README.md")
    
    return True


def troubleshoot():
    """Troubleshoot common issues"""
    print("\n" + "="*60)
    print("TROUBLESHOOTING")
    print("="*60 + "\n")
    
    issues = {
        "ImportError": "Install dependencies: pip install -r requirements.txt",
        "API Key Error": "Add API keys to .env file. Copy .env.example to .env",
        "Rate Limit": "Wait a few minutes before running again",
        "No Results": "Try a different search term or topic",
        "Connection Error": "Check internet connection and firewall"
    }
    
    for issue, solution in issues.items():
        print(f"{issue}:")
        print(f"  → {solution}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup and troubleshoot Research Agent")
    parser.add_argument("--setup", action="store_true", help="Run setup checks")
    parser.add_argument("--trouble", action="store_true", help="Show troubleshooting guide")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_project()
    elif args.trouble:
        troubleshoot()
    elif args.check:
        print("Checking dependencies...")
        deps_ok, missing = check_dependencies()
        if not deps_ok:
            print(f"\nMissing: {', '.join(missing)}")
    else:
        # Run full setup
        setup_project()
