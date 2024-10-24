from django.shortcuts import render
# for taking responses from Http
from django.http import HttpResponse

#request object = HTTP object
def home(request):
    return HttpResponse('Home page')

def room(request):
    return HttpResponse('ROOM')

