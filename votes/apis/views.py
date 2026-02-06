from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from polls.models import Poll, Option
from votes.models import Vote
from .serializers import VoteSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cast_vote(request):
    serializer = VoteSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    poll = serializer.validated_data["poll"]
    option = serializer.validated_data["option"]

    # Check poll is active
    if not poll.is_active:
        return Response(
            {"error": "Poll is not active"},
            status=status.HTTP_400_BAD_REQUEST
        )

    #  Check option belongs to poll
    if option.poll != poll:
        return Response(
            {"error": "Option does not belong to this poll"},
            status=status.HTTP_400_BAD_REQUEST
        )

    #  Prevent double voting
    if Vote.objects.filter(user=request.user, poll=poll).exists():
        return Response(
            {"error": "You have already voted in this poll"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    Vote.objects.create(
        user=request.user,
        poll=poll,
        option=option
    )

    return Response(
        {"message": "Vote cast successfully"},
        status=status.HTTP_201_CREATED
    )
