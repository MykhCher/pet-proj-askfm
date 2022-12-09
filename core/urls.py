from django.urls import path
from .views import AnswerList, QuestionDetail, QuestCreate, QuestList, like_view, AnswerByUser

urlpatterns = [
    path('', AnswerList.as_view(), name='home'),
    path('question/<int:index>', QuestionDetail.as_view(), name='quest_detail'),
    path('create/<int:adressant_id>', QuestCreate.as_view(), name='quest_create'),
    path('quest_list/<int:profile_id>', QuestList.as_view(), name='quest_list'),
    path('like/', like_view, name='like_answer'),
    path('answers/<int:profile_id>', AnswerByUser.as_view(), name='answers-by-user')
]
