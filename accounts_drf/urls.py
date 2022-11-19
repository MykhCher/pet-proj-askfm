from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import AnswerGet, AnswerDetail, AnswererList, ProfileView, QuestionCreateView

urlpatterns= [
    path("login", obtain_auth_token),
    path('answer-detail/<int:pk>/', AnswerDetail.as_view()),
    path('question_create/<int:pk>/', QuestionCreateView.as_view()),
]

router = routers.SimpleRouter()
router.register(r'answerlist', AnswerGet, basename='answers')
router.register(r'answerers', AnswererList)
router.register(r'profile', ProfileView)