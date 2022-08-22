from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count

from .models import Dashboard
from accounts.models import User
from core.models import Answer, Question
from datetime import datetime

class DashboardAdmin(admin.ModelAdmin):
    change_list_template = 'dashboard_change_list.html'

    def get_user_count(self):
        return User.objects.all().count()

    def get_user_count_aWeek(self):
        last_week = datetime.now().isocalendar()[1] - 1
        total = 0
        for i in User.objects.all():
            if i.date_joined.isocalendar()[1] == last_week:
                total += 1
        return total

    def get_question_count(self):
        return Question.objects.all().count()

    def get_answer_count(self):
        return Answer.objects.all().count()

    def comment_count(self):
        total = Answer.objects.all().aggregate(tot=Count('comments'))['tot']
        return total

    def changelist_view(self, request, extra_context=None):
        context = {
            'users': self.get_user_count(),
            'week_users': self.get_user_count_aWeek(),
            'quests': self.get_question_count(),
            'answers': self.get_answer_count(),
            'comments': self.comment_count()
        }
        return super(DashboardAdmin, self).changelist_view(request, extra_context=context)

admin.site.register(Dashboard, DashboardAdmin)
admin.site.unregister(Group)
