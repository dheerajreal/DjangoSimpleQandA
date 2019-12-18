from django.shortcuts import render, get_object_or_404
from .models import Question, Answer
from django.views.generic import ListView, CreateView
from .forms import QuestionCreateForm, AnswerCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()


class QuestionListView(ListView):
    template_name = "questions/index.html"
    model = Question
    paginate_by = 5


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionCreateForm
    template_name = 'questions/create.html'

    def form_valid(self, form):
        form.instance.asked_by = User.objects.get(username=self.request.user)
        return super().form_valid(form)


def question_detail(request, pk):
    template_name = "questions/detail.html"
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(answer_for=question)
    form = AnswerCreateForm(request.POST or None)
    if form.is_valid():
        form.instance.answer_for = question
        form.instance.answered_by = request.user
        form.save()
        form = AnswerCreateForm()
    context = {
        "object": question,
        "answers": answers,
        "form": form
    }
    return render(request, template_name, context)
