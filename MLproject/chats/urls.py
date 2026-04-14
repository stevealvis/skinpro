from django.urls import path
from . import views

urlpatterns = [

  path('post_feedback', views.post_feedback, name='post_feedback'),
  path('get_feedback', views.get_feedback, name='get_feedback'),
  path('chatbot/message', views.chatbot_message, name='chatbot_message'),
   
]
