from django.shortcuts import render, redirect

def index(request):
    context = {
        "user": {"name": "Claire", "hobbies": ["playing video games", "sleeping", "eating"]}
    }
    return render(request,'renders/index.html', context)

def process(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
    else:
        request.session['user_id'] = 2
    request.POST['email']
    return redirect('/')