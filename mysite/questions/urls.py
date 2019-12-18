from django.urls import path, include

from .views import QuestionListView, QuestionCreateView, question_detail


urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),
    path('create/', QuestionCreateView.as_view(), name="question_create"),
    path('q/<int:pk>/', question_detail, name="question_detail"),



]
