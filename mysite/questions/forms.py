from .models import Question, Answer
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("question_text", "question_description")


class AnswerCreateForm(forms.ModelForm):
    answer_text = forms.CharField(label="Give an Answer",
                                  widget=forms.Textarea(
                                      attrs={
                                          "placeholder": "", 'cols': 80, 'rows': 4
                                      }
                                  ),
                                  )

    class Meta:
        model = Answer
        fields = ("answer_text",)


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", ]
