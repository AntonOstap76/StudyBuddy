from django.shortcuts import render

from .models import Room

'''rooms=[
    {'id': 1,
     'name':'Lets learn python'},
     {'id': 2,
     'name':'Design with me '},
     {'id': 3,
     'name':'Frontend developers'},
]'''

#request object = HTTP object
def home(request):
    #model manager(giving all rooms)
    rooms=Room.objects.all()

#for passing data to templates
    context= {'rooms':rooms}

    return render(request, 'base/home.html',context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request, 'base/room.html', context)

