from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import Answer, Question
from .forms import AnswerCreateForm, QuestionCreateForm

User = get_user_model()

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

    def get(self, request, adressant_id):
        if not self.request.user.is_authenticated:
            # messages.add_message(request, messages.ERROR, 'You must sign in to ask a question')
            response = render(self.request,
                          template_name='blocked.html',
                          context={
                            'body': 'You must sign in to ask a question'
                          })
            
            response.status_code = 404
            return response
        adressant = User.objects.get(pk=adressant_id)
        form = self.form_class()
        context = {'form': form, 'adressant': adressant}
        return render(request, self.template_name, context=context)

    def form_valid(self, form):
        quest = form.save(commit=False) 
        adressant_id=self.request.get_full_path().split('/')[2]
        quest.adressant=User.objects.get(pk=adressant_id)
        quest.author = self.request.user
        quest.save()
        return super().form_valid(form)

class QuestList(View):

    def get(self, request, profile_id):
        if self.request.user is None or self.request.user.pk != profile_id:
            response = render(self.request,
                          template_name='blocked.html',
                          context={
                            'body': '404 Not Found :('
                          })
            response.status_code = 404
            return response
        user=User.objects.get(pk=profile_id)
        questions = Question.objects.get_queryset().filter(adressant=user).order_by('-id')
        paginator = Paginator(questions, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(self.request,
                     template_name='quest_list.html', 
                     context=context)

def like_view(request):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
        success_url = request.POST["url"]
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, 'Sign in to like answers')
            return redirect(success_url)
        
        if answer.likes.filter(id=request.user.id).exists():
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
    return redirect(success_url)

    
class AnswerByUser(ListView):
    model = Answer
    paginate_by = 6

    def get(self, request, profile_id, **kwargs):
        self.queryset = self.model.objects.filter(author_id=profile_id)
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['answer_user'] = User.objects.get(pk=profile_id)
        return render(request, template_name='answerbyuser.html', context=context)
    

class UserList(ListView):
    allow_empty = True
    model = User
    ordering = ['-id']
    paginate_by = 8
    paginator_class = Paginator
    template_name = "userlist.html"

    def get(self, request, *args, **kwargs):
        """Handling search results via overriding `ListView.get()` method."""
        if "search" in request.GET:
            self.object_list = self.get_queryset()
            search_result = request.GET["search"]
            added_list = list()
            print(request.GET)
            for user in self.get_queryset():
                fn = user.first_name
                ln = user.last_name
                email = user.email

                fn_prestate = search_result in fn or search_result in fn.lower() or search_result in fn.upper()
                ln_prestate = search_result in ln or search_result in ln.lower() or search_result in ln.upper()
                email_prestate = search_result in email or search_result in email.lower() or search_result in email.upper()

                fn_state = fn_prestate and request.GET.get('first_name') == 'on'
                ln_state = ln_prestate and request.GET.get('last_name') == 'on'
                email_state = email_prestate and request.GET.get('email') == 'on'
                
                if fn_state or ln_state or email_state:
                    added_list.append(user)
                context = self.get_context_data(object_list=added_list)
                
            return self.render_to_response(context)
        return super().get(request, *args, **kwargs)