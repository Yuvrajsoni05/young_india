from  rest_framework import serializers
from manager_app.models import Event_Data


class EventData(serializers.ModelSerializer):
    class Meta:
        model = Event_Data
        fields = '__all__'



