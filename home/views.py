from django.shortcuts import render
from django.http import HttpResponse


def landing_page(request):
    """Main landing page view"""
    return render(request, 'home/landing.html')


def irc_client(request):
    """IRC client page view"""
    return render(request, 'home/irc_client.html')

def admin_status(request):
    """Admin status page for webserver and IRC server"""
    import sys
    import os
    import datetime
    try:
        from local_irc_server import irc_server_instance
        irc_status = irc_server_instance.get_status()
    except Exception as e:
        irc_status = {'user_count': 0, 'users': [], 'events': [], 'error': str(e)}

    web_status = {
        'pid': os.getpid(),
        'python_version': sys.version,
        'server_time': datetime.datetime.now(),
        'cwd': os.getcwd(),
    }
    return render(request, 'admin/status.html', {
        'web_status': web_status,
        'irc_status': irc_status,
    })
