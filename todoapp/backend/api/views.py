#from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .serializers import ToDoSerializer, ToDoToggleCompleteSerializer
from todo.models import ToDo
# This section is for the SignUp and LogIn views.
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


class ToDoListCreate(generics.ListCreateAPIView):
    # ListAPIView two mandatory attributes, serializer_class and
    # get_queryset.
    # We specify TodoSerializer.
    
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user).order_by('-created')
    
    def perform_create(self, serielizer):
        # Serializer holds a django model.
        serielizer.save(user=self.request.user)

class ToDoRetrievUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # User can only update, delet own posts
        return ToDo.objects.filter(user=user)

class ToDoToggleComplete(generics.UpdateAPIView):
    serializer_class = ToDoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user)
    
    def perform_update(self, serializer):
        # Update the completed field of the ToDo object.
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save()

@csrf_exempt
def SignUp(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # Data is a dictionary.
            user = User.objects.create_user(
                data['username'],
                password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error': 'Username taken. Choose another username'},
                status=400)

@csrf_exempt
def Login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            request, 
            username=data['username'], 
            password=data['password'])
        if user is None:
            return JsonResponse(
                {'error': 'Unable to login. Please check username and password'},
                status=400)
        else: # return user token
            try:
                token = Token.objects.get(user=user)
            except: # If token not in db, create one.
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)