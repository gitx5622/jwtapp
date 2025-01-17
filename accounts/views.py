#views/user.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .utils import JsonReader
from .voters import UserVoter
from django.urls import reverse
import json
import requests


@api_view(['GET', 'POST'])
def api_admin_user_index(request):

    # voter = UserVoter(request)
    # if not voter.is_superuser():
    #     return Response({'error': "User API is not allowed by non admin user"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JsonReader.read_body(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_admin_user_detail(request, pk):
  
    voter = UserVoter(request)
    if not voter.is_superuser():
        return Response({'error': "User API is not allowed by non admin user"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': "User " + pk + " does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JsonReader.read_body(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#views/registration.py
@api_view(['POST'])
def api_login(request):
    
    data = JsonReader.read_body(request)

    response_login = requests.post(
        request.build_absolute_uri(reverse('obtain_jwt_token')),
        data=data
    )
    response_login_dict = json.loads(response_login.content)
    return Response(response_login_dict, response_login.status_code)
    
#views/user.py
@api_view(['GET', 'PUT'])
def api_user_detail(request, pk):
  
    try:
        user_inst = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    voter = UserVoter(request)
    if not voter.user_can_manage_me(user_inst):
        return Response({'error': "User API is not allowed"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user_inst)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JsonReader.read_body(request)
        if 'is_staff' in data:
            if not voter.is_superuser():
                return Response({'error': "Non admin cannot update admin attributes"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user_inst, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

