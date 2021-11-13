from django.urls import path
from django.urls.resolvers import URLPattern 
from .views import Index 

urlpatterns = [
    path('', Index.as_view(), name="index")
]