from .models import Question, Answer, QuestionReport
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("question_text", "question_description")


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("answer_text",)


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", ]


class QuestionReportForm(forms.ModelForm):
    class Meta:
        model = QuestionReport
        fields = ["report_description"]
