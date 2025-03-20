from django.urls import path
from .views import ChatbotResponseAPIView

urlpatterns = [
    path('chat/', ChatbotResponseAPIView.as_view(), name='chatbot-response'),
]
