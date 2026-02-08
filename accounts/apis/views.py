from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import userSerializer

@api_view(['POST'])
def register_user(request):
    serializer = userSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "user": userSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request):
    serializer = userSerializer(
        request.user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Profile updated successfully",
                "user": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_my_account(request):
    request.user.delete()
    return Response({"Message: You have successfully deleted your account."}, status= status.HTTP_204_NO_CONTENT)