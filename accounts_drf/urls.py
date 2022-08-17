from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import AnswerGet

urlpatterns= [
    path("login", obtain_auth_token),
]

router = routers.SimpleRouter()
router.register(r'answer', AnswerGet, basename='answers')