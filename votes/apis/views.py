from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import voteSerializer


# Create your views here.

@api_view(['GET'])
def getVotes(request):
    serializers = voteSerializer(many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

