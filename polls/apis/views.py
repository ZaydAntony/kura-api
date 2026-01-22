from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from polls.models import Poll
from .serializers import pollSerializer


# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def postPolls(request):
    polls = Poll.objects.all()
    serializer = pollSerializer(data= request.data)
    if serializer.is_valid(): # my validation check
        serializer.save() #Saving the data to db
    return Response(serializer.data)


@api_view(['GET'])
def getPolls(request):
    polls = Poll.objects.all()
    serializer = pollSerializer(polls, many=True)
    return Response(serializer.data)
