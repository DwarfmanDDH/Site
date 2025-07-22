#!/usr/bin/env python
"""
Kalashnikoff Site - Django application with IRC client
"""
import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False
    return True

def setup_django():
    """Set up Django environment and run migrations"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    try:
        from django.core.management import execute_from_command_line
        
        # Run migrations
        print("Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Migrations completed")
        
        return True
    except ImportError as exc:
        print(f"✗ Django not installed: {exc}")
        return False

def main():
    """Main application entry point"""
    print("🚀 Starting Kalashnikoff Site...")
    print("=" * 50)
    
    # Check if requirements are installed
    try:
        import django
        from channels.routing import ProtocolTypeRouter
    except ImportError:
        print("📦 Installing requirements...")
        if not install_requirements():
            sys.exit(1)
    
    # Setup Django
    if not setup_django():
        sys.exit(1)
    
    # Start the server
    print("\n🌐 Starting development server...")
    print("📱 Landing page: http://127.0.0.1:8080/")
    print("💬 IRC Client: http://127.0.0.1:8080/irc/")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    try:
        from django.core.management import execute_from_command_line
        # Use daphne for ASGI support (WebSockets)
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8080'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"✗ Error starting server: {e}")

if __name__ == '__main__':
    main()