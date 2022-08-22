from re import template
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from validate_email import validate_email
from .forms import UserCreateForm, CustomAuthencticationForm, ProfileEditForm
from .token import account_activation_token


def success(request):
    return render (request, 'success.html')

def invalid_token(request):
    return render (request, 'invalid_token.html')

def activation_reminder(request):
    return render(request, 'activation_reminder.html')

class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('invalid_token')

def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string('acc_activate_email.html',
        {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user),
            'protocol' : 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    return email.send()

class RegisterFormView(FormView):
    form_class = UserCreateForm
    success_url = reverse_lazy('success')
    template_name = "register.html"

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect('register')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        request = self.request
        activate_email(request, user, form.cleaned_data.get('email'))
        return super().form_valid(form)

class LoginFormView(FormView):
    form_class = CustomAuthencticationForm
    success_url = reverse_lazy('home')
    template_name = 'login.html'

    def form_invalid(self, form):
        return redirect('reminder')

    def form_valid(self, form):
        self.user = form.get_user()
        if self.user.status == 'b':
            return render(self.request,
                          template_name='blocked.html',
                          context={
                            'body': 'The user was blocked.'
                          })
        login(self.request, self.user)
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))

class EditProfileView(FormView):
    form_class=ProfileEditForm
    template_name='edit_profile.html'

    def get(self, request):
        user = self.request.user
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birth_date': user.birth_date,
            'town': user.town
        }
        form = self.form_class(initial=initial)
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        user = self.request.user
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birth_date': user.birth_date,
            'town': user.town
        }
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, message='User profile info successfully altered!')
            return redirect('profile/'+str(user.id))

class CheckProfileView(View):
    template_name = 'check_profile.html'
    User = get_user_model()
    def get(self, request, profile_id):
        profile = self.User.objects.get(pk=profile_id)
        if profile.status == 'b':
            return render(self.request,
                          template_name='blocked.html',
                          context={
                            'body': 'The user was blocked.'
                          })
        context = {'profile': profile}
        return render(request, self.template_name, context=context)
    
            

        
