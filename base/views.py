from django.shortcuts import render,redirect

from .models import Room

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
    #model manager(giving all rooms)
    rooms=Room.objects.all()

#for passing data to templates
    context= {'rooms':rooms}

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
