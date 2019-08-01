from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

def index(request):
    template = loader.get_template('login/index.html')
    context = {
        'partners': '',
    }
    return HttpResponse(template.render(context, request))

def submit(request):
    return redirect('home:index')