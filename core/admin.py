from django.contrib import admin
from .models import Question, Answer, Comment


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_author_name', 'get_question', 'body', 'likes_count', 'comments_count')
    search_fields = ('get_question', 'body')
    fields = ['get_question', 'body', 'get_author_name', 'likes_count', 'comments_count']
    readonly_fields = ['get_question', 'get_author_name', 'likes_count', 'comments_count']


admin.site.register(Answer, AnswerAdmin)
