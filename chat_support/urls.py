from django.urls import path
from . import views


app_name = 'chat_support'


urlpatterns = [

    path(
        '',
        views.chat_page,
        name='chat'
    ),

    path(
        'send/',
        views.send_message,
        name='send_message'
    ),

]