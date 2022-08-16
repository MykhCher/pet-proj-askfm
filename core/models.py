from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    adressant = models.ForeignKey(User, related_name='adressant', on_delete=models.CASCADE,
                                null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)