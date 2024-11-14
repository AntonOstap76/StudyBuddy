from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm


#new usercreation form
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name', 'username','email', 'password1', 'password2']
    

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
        fields=['name', 'avatar', 'username', 'email','bio']