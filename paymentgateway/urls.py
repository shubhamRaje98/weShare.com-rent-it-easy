from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns =[
    path('', home, name='home'),

]