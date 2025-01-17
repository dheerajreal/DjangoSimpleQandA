from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from .forms import AnswerCreateForm, QuestionCreateForm, QuestionReportForm
from .models import Answer, Question

User = get_user_model()


class QuestionListView(ListView):
    template_name = "questions/index.html"
    model = Question
    paginate_by = settings.PAGINATE_BY
    queryset = Question.objects.all().select_related(
        "asked_by",
    ).prefetch_related(
        "likes"
    ).prefetch_related(
        Prefetch(
            'answer_set'
        )
    )


class QuestionListByAnswerCount(ListView):
    template_name = "questions/index.html"
    queryset = Question.objects.annotate(
        ans_count=Count('answer')
    ).order_by("-ans_count").select_related(
        "asked_by",
    ).prefetch_related(
        "likes"
    ).prefetch_related(
        Prefetch(
            'answer_set'
        )
    )

    paginate_by = settings.PAGINATE_BY


class QuestionListByLikesCount(ListView):
    template_name = "questions/index.html"
    queryset = Question.objects.annotate(
        like_count=Count('likes')
    ).order_by("-like_count").select_related(
        "asked_by",
    ).prefetch_related(
        "likes"
    ).prefetch_related(
        Prefetch(
            'answer_set'
        )
    )

    paginate_by = settings.PAGINATE_BY


class AskedQuestionListView(LoginRequiredMixin, ListView):
    template_name = "questions/index.html"
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return Question.objects.filter(
            asked_by=self.request.user
        ).select_related(
            "asked_by",
        ).prefetch_related(
            "likes"
        ).prefetch_related(
            Prefetch(
                'answer_set'
            )
        )


class LikedQuestionListView(LoginRequiredMixin, ListView):
    template_name = "questions/index.html"
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return Question.objects.filter(
            likes=self.request.user
        ).select_related(
            "asked_by",
        ).prefetch_related(
            "likes"
        ).prefetch_related(
            Prefetch(
                'answer_set'
            )
        )


class UnansweredQuestionListView(LoginRequiredMixin, ListView):
    template_name = "questions/index.html"
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return Question.objects.filter(
            answer=None
        ).select_related(
            "asked_by",
        ).prefetch_related(
            "likes"
        ).prefetch_related(
            Prefetch(
                'answer_set'
            )
        )


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
    answers = Answer.objects.filter(answer_for=question).select_related(
        # "answered_by",
    )
    form = AnswerCreateForm(request.POST or None)
    if form.is_valid() and request.user.is_authenticated:
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


@login_required
def recent_user_questions(request, user_name):
    template_name = "user/questions.html"
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        raise Http404
    queryset = Question.objects.filter(
        asked_by=user
    ).select_related(
    ).prefetch_related(
    )[:5]
    context = {
        "object_list": queryset,
        "user": user
    }
    return render(request, template_name, context)


@login_required
def recent_user_answers(request, user_name):
    template_name = "user/answers.html"
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        raise Http404
    queryset = Answer.objects.filter(answered_by=user).select_related(
        "answered_by", "answer_for"
    )[:5]
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
def question_like(request, pk):
    if request.method == 'POST':

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
    else:
        return HttpResponseForbidden("Not allowed")


@login_required
def question_report(request, pk):
    template_name = "questions/report.html"
    user = request.user
    question = get_object_or_404(Question, pk=pk)
    form = QuestionReportForm(request.POST or None)
    if form.is_valid():
        form.instance.question = question
        form.instance.user = user
        form.save()
        return redirect(question_detail, pk=pk)
    context = {
        "form": form
    }
    return render(request, template_name, context)


class QuestionSearchView(LoginRequiredMixin, ListView):
    template_name = "questions/index.html"

    # paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        search_term = ""
        queryset = Question.objects.annotate(
            like_count=Count('likes')
        ).order_by("-like_count").select_related(
            "asked_by",
        ).prefetch_related(
            "likes"
        ).prefetch_related(
            Prefetch(
                'answer_set'
            )
        )
        search_term = self.request.GET.get('q', '')
        queryset = queryset.filter(
            Q(question_text__icontains=search_term)
            |
            Q(question_description__icontains=search_term)
        )[:20]

        # queryset = queryset.filter(question_description__icontains=search_term)
        return queryset
