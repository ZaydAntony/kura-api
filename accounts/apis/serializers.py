from rest_framework import serializers
from accounts.models import User


class userSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'role')

        #password hashing
        def create(self, validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password) #hashing
            user.save()
            return user