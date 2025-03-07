from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST,
HTTP_404_NOT_FOUND,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT)
from rest_framework.authtoken.models import Token
from .serializers import UserSerializers

# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))

def user_signup(request):

    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not name:
        return Response({'error':'Name field required.'},status=HTTP_400_BAD_REQUEST)
    elif not email:
        return Response({'error':'Please provide an email address in the proper format.'},status=HTTP_400_BAD_REQUEST)
    elif not password:
        return Response({'error':'password field is required'},status=HTTP_400_BAD_REQUEST)

   
    if User.objects.filter(email__exact=email).exists():
        return Response({'error':'Email already exists'},status=HTTP_409_CONFLICT)
    else:   
        user = User(email = email,username = email,first_name = name ) 
        user.set_password(password)
        user.save()
        return Response({'message':'User Created'},status=HTTP_201_CREATED)
    

@api_view(['POST'])
@permission_classes((AllowAny,))

def user_login(request):
    
    email = request.data.get('email')
    password = request.data.get('password')

    if not email:
        return Response({'error':'Please provide an email address in the proper format.'},status=HTTP_400_BAD_REQUEST)
    elif not password:
        return Response({'error':'password field is required'},status=HTTP_400_BAD_REQUEST)

    is_user = authenticate(username = email,password = password)
    if is_user:
        login(request,is_user)
        token,_ = Token.objects.get_or_create(user = is_user)
        return Response({'token':token.key,'message':'logined successfully.'},status=HTTP_200_OK)
    else:
        return Response({'error':'Invalid Credentials.'},status=HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def user_profile(request):
    user = request.user
    user_data = User.objects.get(username = user )
    
    if not user_data:
        return Response({'error':'Unauthorized user.Please provide valid token'},status=HTTP_401_UNAUTHORIZED)
    else:

        serialized_data = UserSerializers(user_data)
    
        return Response(serialized_data.data,status=HTTP_200_OK)
        


