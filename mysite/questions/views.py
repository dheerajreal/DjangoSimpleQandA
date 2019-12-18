from django.shortcuts import render
from .models import Question
from django.views.generic import ListView

# Create your views here.


def index(request):
    return render(request, "base.html")


class QuestionListView(ListView):
    template_name = "questions/index.html"
    model = Question
    paginate_by = 5
