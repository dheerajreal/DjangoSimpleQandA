from django.urls import path

from .views import (QuestionCreateView, QuestionListView, QuestionUpdateView,
                    question_detail, recent_user_questions,
                    recent_user_answers, specific_user_detail
                    )

urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),
    path('create/', QuestionCreateView.as_view(), name="question_create"),
    path('q/<int:pk>/', question_detail, name="question_detail"),
    path('q/<int:pk>/edit', QuestionUpdateView.as_view(),
         name="question_edit"),


    path('user/<str:user_name>/questions', recent_user_questions,
         name="user_questions_list"),
    path('user/<str:user_name>/answers', recent_user_answers,
         name="user_answers_list"),
    path('user/<str:user_name>/', specific_user_detail,
         name="user_detail"),
]
