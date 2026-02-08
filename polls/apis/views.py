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
from .serializers import PollSerializer


# Create your views here.
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_poll(request):
    serializer = PollSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(createdby=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def list_polls(request):
    polls = Poll.objects.filter(is_active=True).prefetch_related("options")
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def poll_detail(request, poll_id):
    try:
        poll = Poll.objects.prefetch_related("options").get(
            id=poll_id,
            is_active=True
        )
    except Poll.DoesNotExist:
        return Response(
            {"detail": "Poll not found"},
            status=404
        )

    serializer = PollSerializer(poll)
    return Response(serializer.data)


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
