from django.urls import path, include

from . import views

urlpatterns = [
    path('kinnaver/all/', views.kinnaver_all , name='kinnaver_all'),
    path('question/search/', views.QuestionSearch.as_view()),
    path('comment/auto/', views.AutoCommentAPI.as_view()),
]