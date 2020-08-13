from django.urls import path

from .views import (QuestionCreateView, QuestionListByAnswerCount,
                    QuestionListByLikesCount, QuestionListView,
                    QuestionUpdateView, question_detail, question_like,
                    question_report, recent_user_answers,
                    recent_user_questions, specific_user_detail,
                    user_profile_update)

urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),
    path('create/', QuestionCreateView.as_view(), name="question_create"),
    path('q/<int:pk>/', question_detail, name="question_detail"),
    path('q/<int:pk>/edit', QuestionUpdateView.as_view(),
         name="question_edit"),
    path('q/<int:pk>/like', question_like,
         name="question_like"),
    path('q/<int:pk>/report', question_report,
         name="question_report"),




    path('user/<str:user_name>/questions', recent_user_questions,
         name="user_questions_list"),
    path('user/<str:user_name>/answers', recent_user_answers,
         name="user_answers_list"),
    path('user/<str:user_name>/', specific_user_detail,
         name="user_detail"),



    path('most/answered', QuestionListByAnswerCount.as_view(),
         name="sort_by_ans_count"),
    path('most/liked', QuestionListByLikesCount.as_view(),
         name="sort_by_likes_count"),
]
