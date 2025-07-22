#!/usr/bin/env python3
"""
Simple server runner for Kalashnikoff Site
"""
import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"📝 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("🚀 Kalashnikoff Site Server")
    print("=" * 40)
    
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Install dependencies
    if not run_command("py -3 -m pip install Django channels daphne", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("py -3 manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    print("\n🌐 Starting server...")
    print("📍 URLs:")
    print("   Landing page: http://127.0.0.1:8080/")
    print("   IRC Client:   http://127.0.0.1:8080/irc/")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the server
    try:
        subprocess.run("py -3 manage.py runserver 127.0.0.1:8080", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")

if __name__ == "__main__":
    main()
