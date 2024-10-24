from django.db import models
from django.contrib.auth.models import User

# For creating database tables

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

# creating a table for room
class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=200) # can't be left blank
    description=models.TextField(null=True, blank=True) #can be left blank
    #participants=
    updated=models.DateTimeField(auto_now=True)#(take a time step itself)
                                                #take a snapshot of any time  model item  was update
    created=models.DateTimeField(auto_now_add=True)#takes a snapshot when firt time create a room

    def __str__(self):
        return self.name
    

# for creating message table
class Message (models.Model):
    #specify who send a message
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #if room deleted all messages deleted also
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)#(take a time step itself)
                                                #take a snapshot of any time  model item  was update
    created=models.DateTimeField(auto_now_add=True)#takes a snapshot when firt time send a message

    def __str__(self):
        return self.body[0:50]#only 50 char of message


