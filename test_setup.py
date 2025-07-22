#!/usr/bin/env python3
"""
Quick test to verify Django setup
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

try:
    import django
    django.setup()
    
    print("✅ Django setup successful")
    
    # Test imports
    from home.views import landing_page, irc_client
    print("✅ Views imported successfully")
    
    from home.consumers import IRCConsumer
    print("✅ WebSocket consumer imported successfully")
    
    print("🎉 All components loaded successfully!")
    print("\nTo start the server, run:")
    print("  py -3 run_server.py")
    print("  or")
    print("  py -3 manage.py runserver 127.0.0.1:8080")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying to install dependencies...")
    import subprocess
    subprocess.run("py -3 -m pip install Django channels daphne", shell=True)
    print("Dependencies installed. Please run this test again.")

if __name__ == "__main__":
    pass
