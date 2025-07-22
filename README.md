# Kalashnikoff Site

A modern Django-based web application featuring a landing page and a locally hosted IRC client with WebSocket support.

## Features

- **Modern Landing Page**: Clean, responsive design with Bootstrap 5
- **IRC Client**: Full-featured IRC client with real-time messaging
- **WebSocket Support**: Real-time communication using Django Channels
- **Responsive Design**: Works on desktop and mobile devices
- **Easy Setup**: Automated installation and configuration

## Quick Start

### Windows
1. Double-click `start.bat` to automatically install dependencies and start the server
2. Open your browser and go to: http://127.0.0.1:8080/

### Manual Setup
1. Install Python 3.8 or later
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Usage

### Landing Page
Visit http://127.0.0.1:8080/ to see the main landing page with:
- Welcome message and site overview
- Feature showcase
- Navigation to IRC client

### IRC Client
Visit http://127.0.0.1:8080/irc/ to access the IRC client:

1. **Connect to IRC Server**:
   ```
   /connect irc.libera.chat 6667 YourNickname
   ```

2. **Join a Channel**:
   ```
   /join #python
   ```

3. **Send Messages**:
   - Type normally to send messages to the current channel
   - Use `/msg username message` for private messages

### Popular IRC Servers
- **Libera.Chat**: `irc.libera.chat:6667` (General programming channels)
- **OFTC**: `irc.oftc.net:6667` (Open and Free Technology Community)

### Common IRC Commands
- `/connect <server> <port> <nickname>` - Connect to an IRC server
- `/join #<channel>` - Join a channel
- `/msg <target> <message>` - Send a private message
- `/quit` - Disconnect from server

## Technical Details

### Architecture
- **Backend**: Django 4.2+ with Channels for WebSocket support
- **Frontend**: Bootstrap 5, Font Awesome, vanilla JavaScript
- **WebSockets**: Real-time communication between browser and IRC servers
- **Database**: SQLite (for development)

### File Structure
```
Site/
├── app.py                 # Main application launcher
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── start.bat             # Windows startup script
├── mysite/               # Django project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   ├── asgi.py           # ASGI configuration for WebSockets
│   └── wsgi.py           # WSGI configuration
├── home/                 # Main Django app
│   ├── views.py          # Page views
│   ├── urls.py           # App URL routing
│   ├── consumers.py      # WebSocket consumers for IRC
│   └── routing.py        # WebSocket routing
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── home/
│       ├── landing.html  # Landing page
│       └── irc_client.html # IRC client interface
└── static/              # Static files (CSS, JS, images)
    └── css/
        └── style.css     # Custom styles
```

### WebSocket Implementation
The IRC client uses WebSockets to maintain a persistent connection between the browser and the Django backend, which then connects to IRC servers using standard TCP sockets.

## Development

### Adding New Features
1. Modify templates in `templates/home/`
2. Add new views in `home/views.py`
3. Update URL routing in `home/urls.py`
4. Add styles in `static/css/style.css`

### Extending IRC Functionality
- Modify `home/consumers.py` to add new IRC commands
- Update the JavaScript in `irc_client.html` for new UI features

## Requirements

- Python 3.8+
- Django 4.2+
- Django Channels 4.0+
- Modern web browser with WebSocket support

## Security Notes

- This is a development server - not suitable for production
- IRC connections are not encrypted by default
- Consider using SSL/TLS for production deployments

## License

This project is for educational and personal use.
