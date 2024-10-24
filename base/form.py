from django.forms import ModelForm
from .models import Room

#form for the room
class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields= '__all__'