from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from .models import Answer, Question
from .forms import AnswerCreateForm, QuestionCreateForm
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

class AnswerList(View):
    def get(self, request):
        
        answers = Answer.objects.get_queryset().order_by('-id')
        for i in answers:
            if i.author.status == 'b':
                answers = answers.exclude(pk=i.pk)
        paginator = Paginator(answers, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        if "search" in request.GET:
            search=request.GET['search']
            answers=Answer.objects.filter(body__icontains=search)
            return render(self.request,
                     template_name='home.html', 
                     context={'page_obj': answers})
        return render(self.request,
                     template_name='home.html', 
                     context=context)
    
    
class QuestionDetail(View):
    form_class=AnswerCreateForm
    template_name = 'quest_detail.html'
    
    def get(self, request, index):
        question = Question.objects.get(pk=index)
        form = self.form_class
        return render(request, self.template_name, context={'quest': question, 'form': form})

    def post(self, request, index):
        user = self.request.user
        form = self.form_class(request.POST)
        question = Question.objects.get(pk=index)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.author = user
            ans.body = form.cleaned_data['body']
            ans.question = question
            ans.save()  
        return render(request, self.template_name, context={'quest': question})

class QuestCreate(FormView):
    form_class = QuestionCreateForm
    template_name = 'quest_create.html'
    success_url = reverse_lazy('home')
    User = get_user_model()

    def get(self, request, adressant_id):
        if not self.request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, 'You must sign in to ask a question')
            return redirect('http://127.0.0.1:8000/account/profile/'+str(adressant_id)) 
        adressant = self.User.objects.get(pk=adressant_id)
        form = self.form_class()
        context = {'form': form, 'adressant': adressant}
        return render(request, self.template_name, context=context)

    def form_valid(self, form):
        quest = form.save(commit=False) 
        adressant_id=self.request.get_full_path().split('/')[2]
        quest.adressant=self.User.objects.get(pk=adressant_id)
        quest.author = self.request.user
        quest.save()
        return super().form_valid(form)

class QuestList(View):
    def get(self, request, profile_id):
        user=get_user_model().objects.get(pk=profile_id)
        questions = Question.objects.get_queryset().filter(adressant=user).order_by('-id')
        paginator = Paginator(questions, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(self.request,
                     template_name='quest_list.html', 
                     context=context)
