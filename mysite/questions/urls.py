from django.urls import path, include

from .views import QuestionListView, QuestionCreateView


urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),
    path('create/', QuestionCreateView.as_view(), name="question_create"),


]
