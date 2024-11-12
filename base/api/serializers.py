from rest_framework.serializers import ModelSerializer
from base.models import Room

# for taking model and turn it into a json object and I can return that

class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'
