from rest_framework import serializers
from authentication.serializers import UserSerializer

from quiz_app.serializers import AnswerSerializer, QuestionSerializer, QuizSerializer
from .models import QuizPerformance, QuizTry



class QuizTrySerializer(serializers.ModelSerializer):
    owner_try = UserSerializer(read_only=True)

    class Meta:
        model=QuizTry 
        fields=[
            'score',
            'started_at',
            'finished_at',
            'status',
            'quiz',
            'owner',
            'owner_try',

        ]

class QuizPerformanceSerializer(serializers.ModelSerializer):
    quiz_try = QuizTrySerializer(read_only = True)
    question = QuestionSerializer(read_only = True)
    answer = AnswerSerializer(read_only = True)
    class Meta:
        model= QuizPerformance 
        fields=[
            'quiz_try',
            # 'owner',
            'question',
            'answer',
        ]