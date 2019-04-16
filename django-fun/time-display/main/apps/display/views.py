from django.shortcuts import render
from datetime import datetime

def index(request):
    context = {
        "time": datetime.now().strftime('%b %d, %Y %I:%M %p')
    }
    return render(request, 'display/index.html', context)