from django.urls import path
from .views import message_list, respond_message

urlpatterns = [
    path('messages/', message_list, name='message_list'),
    path('messages/<uuid:uuid>/respond/', respond_message, name='respond_message'),
]
