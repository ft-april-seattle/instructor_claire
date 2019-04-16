from django.shortcuts import render
from django.utils.crypto import get_random_string


def index(request):
    if 'count' not in request.session:
        request.session['count'] = 1
    else:
        request.session['count'] += 1

    context = {
        "word": get_random_string(length=14)
    }
    return render(request, 'generate/index.html', context)
