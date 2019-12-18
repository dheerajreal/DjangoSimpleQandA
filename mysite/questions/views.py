from django.shortcuts import render, get_object_or_404
from .models import Question
from django.views.generic import ListView, CreateView
from .forms import QuestionCreateForm
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


def index(request):
    return render(request, "base.html")


class QuestionListView(ListView):
    template_name = "questions/index.html"
    model = Question
    paginate_by = 5


class QuestionCreateView(CreateView):
    form_class = QuestionCreateForm
    template_name = 'questions/create.html'

    def form_valid(self, form):
        form.instance.asked_by = User.objects.get(username=self.request.user)
        return super().form_valid(form)


def question_detail(request, pk):
    template_name = "questions/detail.html"
    question = get_object_or_404(Question, pk=pk)
    context = {
        "object": question
    }
    return render(request, template_name, context)
