from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
User = get_user_model()


class Question(models.Model):
    question_text = models.CharField(max_length=128)
    question_description = models.TextField(null=True, max_length=256)
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    asked_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-asked_datetime']


class Answer(models.Model):
    answer_text = models.TextField(max_length=256)
    answer_for = models.ForeignKey(Question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answered_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ['-answered_datetime']
