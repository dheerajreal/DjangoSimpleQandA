from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from .forms import AnswerCreateForm, QuestionCreateForm, UserEditForm
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


def recent_user_questions(request, user_name):
    template_name = "user/questions.html"
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        raise Http404
    queryset = Question.objects.filter(asked_by=user)[:5]
    context = {
        "object_list": queryset,
        "user": user
    }
    return render(request, template_name, context)


def recent_user_answers(request, user_name):
    template_name = "user/answers.html"
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        raise Http404
    queryset = Answer.objects.filter(answered_by=user)[:5]
    context = {
        "object_list": queryset,
        "user": user
    }
    return render(request, template_name, context)


@login_required
def specific_user_detail(request, user_name):
    template_name = "user/detail.html"
    try:
        user = User.objects.get(username=user_name)

    except User.DoesNotExist:
        raise Http404

    context = {

        "user": user
    }
    return render(request, template_name, context)


@login_required
def user_profile_update(request):
    template_name = "accounts/edit.html"
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        raise Http404
    form = UserEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect("user_detail", user.username)
    context = {
        "user": user,
        "form": form,
    }
    return render(request, template_name, context)


@login_required
def question_like(request, pk):
    user = request.user
    r = {"pk": pk, "Action": None}
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        r["Action"] = "404"
        return JsonResponse(r, status=404)

    if (question.likes.filter(username=user)):
        question.likes.remove(user)
        r["Action"] = "Like"
        return JsonResponse(r)
    else:
        question.likes.add(user)
        r["Action"] = "Unlike"
        return JsonResponse(r)
