from django.contrib import admin
from .models import Question, Answer, QuestionReport

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionReport)
