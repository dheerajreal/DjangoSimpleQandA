from .models import Question, Answer
from django import forms


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
