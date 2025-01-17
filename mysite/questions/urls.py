from django.urls import path

from .views import (
    AskedQuestionListView,
    LikedQuestionListView,
    QuestionCreateView,
    QuestionListByAnswerCount,
    QuestionListByLikesCount,
    QuestionListView,
    QuestionUpdateView,
    UnansweredQuestionListView,
    question_detail,
    question_like,
    question_report,
    recent_user_answers,
    recent_user_questions,
    specific_user_detail,
    QuestionSearchView
)

urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),
    path('q/search/',
         QuestionSearchView.as_view(), name="question_search"),
    path('q/create/', QuestionCreateView.as_view(), name="question_create"),
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



    path('view/mostanswered', QuestionListByAnswerCount.as_view(),
         name="sort_by_ans_count"),
    path('view/mostliked', QuestionListByLikesCount.as_view(),
         name="sort_by_likes_count"),
    path('view/asked', AskedQuestionListView.as_view(),
         name="asked_by_user"),
    path('view/liked', LikedQuestionListView.as_view(),
         name="liked_questions_list"),
    path('view/unanswered', UnansweredQuestionListView.as_view(),
         name="unanswered_questions_list"),
]
