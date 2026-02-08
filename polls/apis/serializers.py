from rest_framework import serializers
from polls.models import Poll, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("id", "text")


class PollSerializer(serializers.ModelSerializer):
    createdby = serializers.StringRelatedField(read_only=True)
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            "id",
            "title",
            "description",
            "startTime",
            "endTime",
            "is_active",
            "createdby",
            "options",
        )

    def create(self, validated_data):
        options_data = validated_data.pop("options")
        poll = Poll.objects.create(**validated_data)

        for option in options_data:
            Option.objects.create(poll=poll, **option)

        return poll
