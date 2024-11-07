from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .models import Room, Topic, Message

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .form import RoomForm,UserForm

'''rooms=[
    {'id': 1,
     'name':'Lets learn python'},
     {'id': 2,
     'name':'Design with me '},
     {'id': 3,
     'name':'Frontend developers'},
]'''

#for login page
def loginPage(request):

    page='login'

    #don`t want allow a user to relogin 
    if request.user.is_authenticated:
        return redirect('home')

    #if user put their information
    if request.method=='POST':
        #get information
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        #checking if this user already exist
        #if user does not exist
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        #if user exist(giving an user object)
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'Username or password does not exist')

    context={'page':page}
    return render(request, 'base/login_register.html', context)

#for logout the user
def logoutUser(request):
    logout(request)
    return redirect('home')

#for register a user
def registerPage(request):
    
    form = UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            # to access the user 
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            #after registration user alredy login
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during  registration')

    return render(request, 'base/login_register.html', {'form':form})


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
    topics=Topic.objects.all()[0:5]

    room_count=rooms.count()

    room_messages=Message.objects.filter(
        Q(room__topic__name__icontains=q)
        )

#for passing data to templates
    context= {'rooms':rooms,
              'topics':topics,
              'room_count':room_count, 
              'room_messages':room_messages}

    return render(request, 'base/home.html',context)

def room(request, pk):
    room=Room.objects.get(id=pk)

#get all comments(messages)
#giving all messages that are related to spesific room
    room_messages=room.message_set.all()

    #adding participants
    participants=room.participants.all()

    if request.method == 'POST':
        #creating a message by what written in the field 
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context={'room':room,
             'room_messages':room_messages,
             'participants':participants}
    return render(request, 'base/room.html', context)

#for user profile page
def userProfile(request, pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,
             'rooms': rooms,
             'room_messages':room_messages, 
             'topics':topics}
    return render(request, 'base/profile.html', context)




# for creating a room 
#restricted for user who is not login(redirected to login page)
@login_required(login_url='login')
def createRoom(request):

    form=RoomForm()
    topics=Topic.objects.all()

    if request.method =='POST':
        topic_name=request.POST.get('topic')
        #if an topic was not created it will create this topic object
        topic, created= Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),

        )
        return redirect('home')


    context={'form': form, 
             'topics':topics}
    return render(request, 'base/room_form.html', context)


#for updating a room
#restricted for user who is not login(redirected to login page)
@login_required(login_url='login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)#to prefill form with room data

    topics=Topic.objects.all()

#checking if the user who want to update a room is the same who create it
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        #if an topic was not created it will create this topic object
        topic, created= Topic.objects.get_or_create(name=topic_name)
        form=RoomForm(request.POST, instance=room)#specify what room to update
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.topic=topic
        room.save()
        return redirect('home')

    context={'form': form,
             'topics':topics,
             'room':room}
    return render(request, 'base/room_form.html', context)


#for deleting room
#restricted for user who is not login(redirected to login page)
@login_required(login_url='login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)

#checking if the user who want to delete a room is the same who create it
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render (request, 'base/delete.html', {'obj':room})

#for deleting a message
#restricted for user who is not login(redirected to login page)
@login_required(login_url='login')
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk)

#checking if the user who want to delete a room is the same who create it
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render (request, 'base/delete.html', {'obj':message})

# for enabeling edit of user page
@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method=='POST':
         form=UserForm(request.POST, instance=user)
         if form.is_valid():
             form.save()
             return redirect('user-profile', pk=user.id)
             


    return render(request, 'base/update-user.html', {'form':form})

#for mobile responsivness
def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    topics=Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

#for mobile responsivness
def activityPage(request):
    room_messages=Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})


