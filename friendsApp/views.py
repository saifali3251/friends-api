from http.client import HTTPResponse
from django.http import JsonResponse
from .models import Friends
from rest_framework import serializers
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from .serializers import FriendSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics,mixins,viewsets
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



total_levels = ['Easy','Medium','Hard']
map_level = [5,4,3]
friends_character = ['Ross','Phoebe','Joey','Monica','Rachel','Chandler']
total_season = ['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10',]
c = 0

def homepage(request):
  return render(request,'index.html')


@api_view(['GET'])
def index(request):
  if request.method == 'GET':
    c = Friends.objects.all()
    c = len(c)
    link = 'https://friends-quotes-alpha-api.herokuapp.com/docs'
    b = f"Welcome to Our FRIENDS Api. Visit {link}  to explore all the APIs. It contains more than {c} quotes. Currently we have Quotes for Season-01 only. We will be adding more quotes in future.Current rate limit is set as 10 calls/hour."
  return Response(b)


@api_view(['GET','POST'])
@permission_classes((IsAuthenticated, ))
def all_quotes(request):
  if request.method == 'GET':
    friends = Friends.objects.all().filter(relevancy__gt=4).order_by('id')
    serializer = FriendSerializer(friends,many=True)
    return Response(serializer.data)
  elif request.method == 'POST':
    serializer = FriendSerializer(data = request.data,many=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


import random
@api_view(['GET'])
def get_random_quote(request,level=None):
  if request.method == 'GET':
    if level is None:
      """This single line randomizing code can be slower than later code"""
      f1 = Friends.objects.order_by('?').filter(relevancy__gt=3).first()
      # c = int(Friends.objects.count())
      # friends = Friends.objects.filter(relevancy__gt=3)
      # l1 = len(friends)
      # id = random.randint(0,l1-1)
      # f1 = friends
    else:
      if level.title() not in total_levels:
        x = f'Must be among {total_levels}, got {level}'
        return Response(x,status=status.HTTP_404_NOT_FOUND)
      friends = Friends.objects.filter(relevancy=map_level[total_levels.index(level.title())])
      l1 = len(friends)
      id = random.randint(0,l1-1)
      print(id)
      f1 = friends[id]
    serializer = FriendSerializer(f1)
    return Response(serializer.data)


@api_view(['GET'])
def random_quote_by_character(request,character):
  if request.method == 'GET':
    if character.title() not in friends_character:
      x = f'Must be among {friends_character}, got {character}'
      return Response(x,status=status.HTTP_404_NOT_FOUND)

    # friends = Friends.objects.order_by('?').filter(character=character,relevancy__gt=3).first()
    friends = random.choice(Friends.objects.all().filter(character=character.title(),relevancy__gt=3))
    # friends = Friends.objects.filter(character=character)
    # l1 = len(friends)
    # id = random.randint(0,l1)
    # f1 = friends[id]
    # print(f1.id)
    serializer = FriendSerializer(friends)
    return Response(serializer.data)



@api_view(['GET'])
def random_quote_by_season_character(request,season,character):
  if request.method == 'GET':
    if season.title() not in total_season:
      x = f'Must be among {total_season}, got {season}'
      return Response(x,status=status.HTTP_404_NOT_FOUND)
    if character.title() not in friends_character:
      x = f'Must be among {friends_character}, got {character}'
      return Response(x,status=status.HTTP_404_NOT_FOUND)

    friends = Friends.objects.filter(season=season.title(),character=character.title(),relevancy__gt=3)
    l1 = len(friends)
    print(l1)
    id = random.randint(0,l1-1)
    f1 = friends[id]
    serializer = FriendSerializer(f1)
    return Response(serializer.data)



@api_view(['GET'])
def random_quote_by_season(request,season):
  if request.method == 'GET':
    if season.title() not in total_season:
      x = f'Must be among {total_season}, got {season}'
      return Response(x,status=status.HTTP_404_NOT_FOUND)

    friends = Friends.objects.filter(season=season.title(),relevancy__gt=3)
    l1 = len(friends)
    id = random.randint(0,l1-1)
    f1 = friends[id]
    serializer = FriendSerializer(f1)
    return Response(serializer.data)


@api_view(['GET'])
def all_characters_by_season(request,season):
  if request.method == 'GET':
    if season.title() not in total_season:
      x = f'Must be among {total_season}, got {season}'
      return Response(x,status=status.HTTP_404_NOT_FOUND)

    friends = Friends.objects.values('character').annotate(total_count=Count('character')).filter(season=season.title())
    friend_list = [friends[i]['character'] for i in range(len(friends))]
    return Response(friend_list)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def quotes_count_by_relevancy(request,value):
  if request.method == 'GET':
    friends = Friends.objects.filter(relevancy=value).count()
    # serializer = FriendSerializer(friends)
    return Response(friends)
