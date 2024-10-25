from django.shortcuts import render,redirect

from django.db.models import Q
from .models import Room, Topic

from .form import RoomForm

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

    q=request.GET.get('q') if request.GET.get('q') != None else ''

    #model manager(giving  rooms where topic name contains q  )
    #searching by topic name or by name of the room
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    

    #get all topics 
    topics=Topic.objects.all()

    room_count=rooms.count()

#for passing data to templates
    context= {'rooms':rooms,
              'topics':topics,
              'room_count':room_count}

    return render(request, 'base/home.html',context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request, 'base/room.html', context)

# for creating a room 
def createRoom(request):

    form=RoomForm

    if request.method =='POST':
        #form know which values to extract from that
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            #after creation of room redirect to home page
            return redirect('home')


    context={'form': form}
    return render(request, 'base/room_form.html', context)

#for updating a room
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)#to prefill form with room data

    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)#specify what room to update
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form': form}
    return render(request, 'base/room_form.html', context)


#for deleting room
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render (request, 'base/delete.html', {'obj':room})
