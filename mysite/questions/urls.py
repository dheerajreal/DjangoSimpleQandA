from django.urls import path

from .views import (QuestionCreateView, QuestionListView, QuestionUpdateView,
                    question_detail)

urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),
    path('create/', QuestionCreateView.as_view(), name="question_create"),
    path('q/<int:pk>/', question_detail, name="question_detail"),
    path('q/<int:pk>/edit', QuestionUpdateView.as_view(), name="question_edit"),


]
