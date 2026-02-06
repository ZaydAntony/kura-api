import requests
from django.conf import settings
from django.shortcuts import render
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from votes.models import Vote
from polls.models import Poll,Option
from .serializers import pollSerializer,optionSerializer


# Create your views here.
@permission_classes([IsAdminUser])
@api_view(['POST'])
def postPolls(request):
    polls = Poll.objects.all()
    serializer = pollSerializer(data= request.data)
    if serializer.is_valid(): # my validation check
        serializer.save(createdby=request.user) #Saving the data to db
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getPolls(request):
    polls = Poll.objects.all()
    serializer = pollSerializer(polls, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAdminUser])
@api_view(['POST'])
def addOptions(request):

    poll_id = request.data.get('poll')
    try:
        poll = Poll.objects.get(id=poll_id, is_active=True)
    except Poll.DoesNotExist:
        return Response(
            {"error": "Invalid or inactive poll"},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = optionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getOptions(request):
    options = Option.objects.all()
    serializer = optionSerializer(options, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def generate_ai_summary(poll_title, results):
    prompt = f"""
    Generate a clear and insightful summary of the poll results.

    Poll: {poll_title}
    Results: {results}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Django Polls Project"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 80
        },
        timeout=15
    )

    data = response.json()
    return data["choices"][0]["message"]["content"]


@api_view(['GET'])
def getResults(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return Response(
            {"message": "Poll does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    options = Option.objects.filter(
        poll=poll
    ).annotate(
        votes_count=Count('vote')
    )

    results = [
        {
            "option_id": option.id,
            "option_text": option.text,
            "votes": option.votes_count
        }
        for option in options
    ]

    ai_summary = generate_ai_summary(poll.title, results)

    return Response({
        "poll": poll.title,
        "results": results,
        "ai_summary": ai_summary
    })
