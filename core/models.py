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

    def __str__(self):
        return f'{self.body}'


class Answer(models.Model):
    author = models.ForeignKey(User, related_name="answer", on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')

    def get_author_name(self):
        return f'{self.author.first_name} {self.author.last_name}'

    def comments_count(self):
        return self.comments.count()

    def likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    body = models.CharField(max_length=250)
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    answer=models.ForeignKey(Answer, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
