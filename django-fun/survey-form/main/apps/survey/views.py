from django.shortcuts import render, redirect

def index(request):
    
    return render(request,'survey/index.html')

def process(request):
    request.session["name"] = request.POST['name']
    request.session["location"] = request.POST['location']
    request.session["language"] = request.POST['language']
    request.session["comments"] = request.POST['comments']

    return redirect('/result')

def result(request):
    if 'count' not in request.session:
        request.session['count'] = 1
    else:
        request.session['count'] += 1

    return render(request, 'survey/result.html')