from django.urls import path, include

from .views import QuestionListView


urlpatterns = [
    path('', QuestionListView.as_view(), name="index"),

]
