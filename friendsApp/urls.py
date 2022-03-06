
import imp
from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import path
# from djangorest.firstProject.firstApp.views import AuthorDetail
from friendsApp import views

urlpatterns = [
    path('',views.homepage,name='index'),
    path('friends/quotes/',views.all_quotes),
    path('friends/random/',views.get_random_quote),
    path('friends/random/level/<str:level>',views.get_random_quote),
    path('friends/level/<int:value>',views.quotes_count_by_relevancy),
    path('friends/random/character/<str:character>',views.random_quote_by_character),
    path('friends/random/season/<str:season>',views.random_quote_by_season),
    path('friends/random/season/character/<str:season>/<str:character>',views.random_quote_by_season_character),
    path('friends/characters/<str:season>',views.all_characters_by_season),

]

