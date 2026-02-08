from rest_framework import serializers
from votes.models import Vote
from polls.models import Poll, Option

class voteSerializer(serializers.Serializer):
    poll = serializers.PrimaryKeyRelatedField(
        queryset=Poll.objects.all()
    )
    option = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all()
    )
