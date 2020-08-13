from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
User = get_user_model()


class QuestionLikes(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class QuestionReport(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_description = models.TextField(
        "Report if you think this question is abusing our service.",
        max_length=256,
        help_text="Required. 256 characters or fewer."
    )

    def __str__(self):
        return f"{self.user}  Reported {self.question}"


class Question(models.Model):
    question_text = models.CharField(
        max_length=128,
        help_text="This is your question. Required. 128 characters or fewer."
    )
    question_description = models.TextField(
        blank=True,
        null=True,
        max_length=256,
        help_text="Describe your question and provide extra details if necessary. Optional. 256 characters or fewer."
    )
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    asked_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited_datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    likes = models.ManyToManyField(
        User, through=QuestionLikes, related_name="likes"
    )

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-asked_datetime']


class Answer(models.Model):
    answer_text = models.TextField(
        help_text="Required. 256 characters or fewer.",
        max_length=256
    )
    answer_for = models.ForeignKey(Question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answered_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ['-answered_datetime']
