from rest_framework import serializers
from manager_app.models import  Event_Data






class EventDataSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Event_Data
        fields = '__all__'
