from rest_framework import serializers
from .models import Question, Answer, Quiz



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer 
        fields=['text', 'image', 'isCorrect', 'question']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model=Question 
        fields=['text', 'image', 'score', 'order', 'quiz','answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,read_only=True)
    class Meta:
        model=Quiz 
        fields=[
            'name',
            'description',
            'max_score',
            'max_time_to_solve',
            'question_quantity',
            'image',
            'status',
            'questions',
            'owner',
            ]
            

    


    