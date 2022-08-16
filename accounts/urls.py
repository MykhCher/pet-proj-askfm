from django.urls import path
from .views import (
    LoginFormView, 
    RegisterFormView, 
    success, 
    activate, 
    invalid_token, 
    LogoutView, 
    activation_reminder,
    EditProfileView,
    CheckProfileView
    )

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('success/', success, name='success'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('success/', invalid_token, name='invalid_token'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activation_reminder', activation_reminder, name='reminder'),
    path('edit', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<int:profile_id>', CheckProfileView.as_view(), name='check_profile')
]
