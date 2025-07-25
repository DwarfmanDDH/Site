import asyncio
import socket


import threading
import time

class SimpleIRCServer:
    def __init__(self, host='127.0.0.1', port=6667):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        self.nicknames = {}  # writer -> nick
        self.events = []     # (timestamp, event, nick, info)
        self.lock = threading.Lock()

    def get_status(self):
        with self.lock:
            users = list(self.nicknames.values())
            events = list(self.events)[-50:]  # last 50 events
        return {
            'user_count': len(users),
            'users': users,
            'events': events,
        }

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        nick = None
        self.clients.add(writer)
        try:
            writer.write(b':localhost NOTICE * :Welcome to the local IRC server!\r\n')
            await writer.drain()
            while True:
                data = await reader.readline()
                if not data:
                    break
                message = data.decode(errors='ignore').strip()
                if message.upper().startswith('NICK'):
                    nick = message.split(' ', 1)[1] if ' ' in message else 'guest'
                    with self.lock:
                        self.nicknames[writer] = nick
                        self.events.append((time.strftime('%Y-%m-%d %H:%M:%S'), 'join', nick, f'{addr} joined'))
                    writer.write(f':localhost 001 {nick} :Welcome to Local IRC!\r\n'.encode())
                    await writer.drain()
                elif message.upper().startswith('USER'):
                    continue
                elif message.upper().startswith('JOIN'):
                    channel = message.split(' ', 1)[1] if ' ' in message else '#test'
                    writer.write(f':localhost JOIN {channel}\r\n'.encode())
                    await writer.drain()
                elif message.upper().startswith('PRIVMSG'):
                    # Echo message to all clients
                    for client in self.clients:
                        if client != writer:
                            client.write(data)
                            await client.drain()
                elif message.upper().startswith('PING'):
                    pong = message.replace('PING', 'PONG')
                    writer.write(f'{pong}\r\n'.encode())
                    await writer.drain()
                elif message.upper().startswith('QUIT'):
                    break
        except Exception:
            pass
        finally:
            self.clients.discard(writer)
            with self.lock:
                if writer in self.nicknames:
                    left_nick = self.nicknames.pop(writer)
                    self.events.append((time.strftime('%Y-%m-%d %H:%M:%S'), 'leave', left_nick, f'{addr} left'))
            writer.close()
            await writer.wait_closed()

    async def start(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f'Local IRC server running on {self.host}:{self.port}')
        async with self.server:
            await self.server.serve_forever()

# Singleton instance for import
irc_server_instance = SimpleIRCServer()
