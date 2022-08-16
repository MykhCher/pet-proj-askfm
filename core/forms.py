from django import forms
from .models import Answer, Question


class QuestionCreateForm(forms.ModelForm):
    body = forms.CharField(label='Detailed description of your question',
                            widget=forms.Textarea(attrs={
                                'class': 'ui input' ,
                                'rows': 5,
                                'placeholder' : 'Detailed description'
                            }))
    
    class Meta:
        model = Question
        fields = ['body']

class AnswerCreateForm(forms.ModelForm):
    body=forms.CharField(label='Your answer', widget=forms.Textarea(attrs={
        'class':'ui input',
        'placehodler': 'Your answer',
        'rows': 1
    }))
    class Meta:
        model=Answer
        fields=['body']
