from django.urls import path
from . import views

urlpatterns = [
    path('start-quiz/',views.QuizTryList.as_view()),
    path('submit-quiz/',views.QuizPerformanceList.as_view()),
    path('finish-quiz/<int:pk>',views.FinishQuiz.as_view() )
]


