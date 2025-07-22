from django.shortcuts import render
from django.http import HttpResponse


def landing_page(request):
    """Main landing page view"""
    return render(request, 'home/landing.html')


def irc_client(request):
    """IRC client page view"""
    return render(request, 'home/irc_client.html')
