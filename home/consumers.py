import asyncio
import json
import socket
from channels.generic.websocket import AsyncWebsocketConsumer


class IRCConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.irc_socket = None
        self.reader = None
        self.writer = None
        
    async def connect(self):
        await self.accept()
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'system',
            'message': 'Connected to IRC client. Use /connect <server> <port> <nickname> to connect to an IRC server.'
        }))

    async def disconnect(self, close_code):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            command = data.get('command', '')
            
            if command.startswith('/connect'):
                parts = command.split()
                if len(parts) >= 4:
                    server = parts[1]
                    port = int(parts[2])
                    nickname = parts[3]
                    await self.connect_to_irc(server, port, nickname)
                else:
                    await self.send_error("Usage: /connect <server> <port> <nickname>")
            
            elif command.startswith('/join'):
                if self.writer:
                    parts = command.split()
                    if len(parts) >= 2:
                        channel = parts[1]
                        self.writer.write(f"JOIN {channel}\r\n".encode())
                        await self.writer.drain()
                    else:
                        await self.send_error("Usage: /join <channel>")
                else:
                    await self.send_error("Not connected to IRC server")
            
            elif command.startswith('/msg'):
                if self.writer:
                    parts = command.split(' ', 2)
                    if len(parts) >= 3:
                        target = parts[1]
                        message = parts[2]
                        self.writer.write(f"PRIVMSG {target} :{message}\r\n".encode())
                        await self.writer.drain()
                        # Echo the message back to the client
                        await self.send(text_data=json.dumps({
                            'type': 'message',
                            'target': target,
                            'message': f"<You> {message}"
                        }))
                    else:
                        await self.send_error("Usage: /msg <target> <message>")
                else:
                    await self.send_error("Not connected to IRC server")
            
            else:
                # Regular message to current channel
                if self.writer and hasattr(self, 'current_channel'):
                    self.writer.write(f"PRIVMSG {self.current_channel} :{command}\r\n".encode())
                    await self.writer.drain()
                    await self.send(text_data=json.dumps({
                        'type': 'message',
                        'target': self.current_channel,
                        'message': f"<You> {command}"
                    }))
                else:
                    await self.send_error("Join a channel first using /join <channel>")
                    
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON received")
        except Exception as e:
            await self.send_error(f"Error: {str(e)}")

    async def connect_to_irc(self, server, port, nickname):
        try:
            self.reader, self.writer = await asyncio.open_connection(server, port)
            
            # Send IRC connection commands
            self.writer.write(f"NICK {nickname}\r\n".encode())
            self.writer.write(f"USER {nickname} 0 * :{nickname}\r\n".encode())
            await self.writer.drain()
            
            self.nickname = nickname
            
            # Start reading from IRC server
            asyncio.create_task(self.read_from_irc())
            
            await self.send(text_data=json.dumps({
                'type': 'system',
                'message': f'Connecting to {server}:{port} as {nickname}...'
            }))
            
        except Exception as e:
            await self.send_error(f"Failed to connect to {server}:{port} - {str(e)}")

    async def read_from_irc(self):
        try:
            while True:
                data = await self.reader.readline()
                if not data:
                    break
                    
                line = data.decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                
                # Handle PING
                if line.startswith('PING'):
                    pong = line.replace('PING', 'PONG')
                    self.writer.write(f"{pong}\r\n".encode())
                    await self.writer.drain()
                    continue
                
                # Parse IRC messages
                await self.parse_irc_message(line)
                
        except Exception as e:
            await self.send_error(f"IRC connection error: {str(e)}")

    async def parse_irc_message(self, line):
        try:
            # Basic IRC message parsing
            if ' PRIVMSG ' in line:
                # Extract sender, target, and message
                parts = line.split(' PRIVMSG ')
                sender_part = parts[0]
                if '!' in sender_part:
                    sender = sender_part.split('!')[0][1:]  # Remove the ':'
                else:
                    sender = sender_part[1:] if sender_part.startswith(':') else sender_part
                
                target_message = parts[1]
                target, message = target_message.split(' :', 1)
                
                await self.send(text_data=json.dumps({
                    'type': 'message',
                    'target': target,
                    'message': f"<{sender}> {message}"
                }))
            
            elif ' JOIN ' in line:
                # Handle JOIN messages
                parts = line.split(' JOIN ')
                sender_part = parts[0]
                if '!' in sender_part:
                    sender = sender_part.split('!')[0][1:]
                else:
                    sender = sender_part[1:] if sender_part.startswith(':') else sender_part
                
                channel = parts[1].strip(':')
                await self.send(text_data=json.dumps({
                    'type': 'system',
                    'message': f"{sender} joined {channel}"
                }))
                
                if sender == self.nickname:
                    self.current_channel = channel
            
            elif ' 001 ' in line or 'Welcome' in line:
                await self.send(text_data=json.dumps({
                    'type': 'system',
                    'message': 'Connected to IRC server! Use /join #channel to join a channel.'
                }))
            
            else:
                # Send raw message for debugging
                await self.send(text_data=json.dumps({
                    'type': 'raw',
                    'message': line
                }))
                
        except Exception as e:
            await self.send_error(f"Error parsing IRC message: {str(e)}")

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
