from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView, UpdateView

from .forms import AnswerCreateForm, QuestionCreateForm
from .models import Answer, Question

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


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = "questions/update.html"
    fields = ["question_text", "question_description"]
    success_url = "/"

    def test_func(self):
        return self.request.user == self.get_object().asked_by

    def form_valid(self, form):
        if self.request.user == form.instance.asked_by:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("Not allowed")


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
