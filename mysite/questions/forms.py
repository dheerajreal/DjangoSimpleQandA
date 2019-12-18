from .models import Question
from django import forms


class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("question_text", "question_description")
