from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

#form for the room
class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields= '__all__'
        exclude=['host', 'participants']

#for for editing user
class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username', 'email']