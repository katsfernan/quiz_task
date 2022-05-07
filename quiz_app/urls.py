from django.urls import path
from . import views

urlpatterns = [
    path('question/',views.QuestionList.as_view()),
    path('question/<int:pk>', views.QuestionDetail.as_view()),

    path('quiz/', views.QuizList.as_view()),
    path('quiz/<int:pk>', views.QuizDetail.as_view()),

    path('answer/', views.AnswerList.as_view()),
    path('answer/<int:pk>', views.AnswerDetail.as_view())
]


