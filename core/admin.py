from django.contrib import admin
from .models import Question, Answer, Comment


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_author_name', 'question', 'body', 'likes_count', 'comments_count')


admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment)
