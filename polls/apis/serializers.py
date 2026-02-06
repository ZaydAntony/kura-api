from rest_framework import serializers
from polls.models import Poll, Option

class pollSerializer(serializers.ModelSerializer):
    createdby = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Poll
        fields = ('title', 'description', 'startTime', 'endTime', 'createdby', 'is_active ')


class optionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Option
        fields = ('id', 'poll', 'text')
        read_only = ('id',)