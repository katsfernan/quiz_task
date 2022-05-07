from .serializers import QuestionSerializer, AnswerSerializer, QuizSerializer
from .models import Question, Answer, Quiz
from django.http import Http404, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User

from django.core.exceptions import PermissionDenied

from decimal import Decimal

@permission_classes([IsAuthenticated])
class QuizList(APIView):

    def get_user(self, pk):
        return User.objects.filter(pk = pk)
        
    def get(self, request):
        quizzes = Quiz.objects.all()
        if not quizzes:
            return Response(status=status.HTTP_204_NO_CONTENT, data={"message":"There is no quizzes created!"})
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        request.data['owner'] = request.user.id
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class QuizDetail(APIView):

    def get_quiz(self, pk):
        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            raise Http404

    def validate_user(self, request, quiz_id):
        try:
            quiz = self.get_quiz(pk=quiz_id)
        except Quiz.DoesNotExist:
            raise HttpResponseBadRequest
        if quiz.owner_id != request.user.id and not request.user.is_staff:
            raise PermissionDenied()

    
    def get(self, pk):
        quiz = self.get_quiz(pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, pk):
        quiz = self.get_quiz(pk)
        self.validate_user(request, pk)
        request.data['owner'] = quiz.owner.id
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        quiz = self.get_quiz(pk)
        self.validate_user(request, pk)
        quiz.delete()
        return Response(status=status.HTTP_200_OK, data={"message":"Quiz deleted successfully!"})
        
@permission_classes([IsAuthenticated])  
class QuestionList(APIView):
    def get(self, pk):
        questions = Question.objects.all()
        if not questions:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            quiz = Quiz.objects.get(pk=request.data['quiz'])
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if quiz.owner_id == request.user.id:
            max_score = quiz.max_score
            max_score = (0 if max_score is None else max_score) + Decimal(request.data['score'])
            quiz.max_score = max_score
            quiz.question_quantity = (0 if quiz.question_quantity is None else quiz.question_quantity) + 1
            quiz.save()
            counter = Question.objects.filter(quiz = request.data['quiz']).count() + 1
            request.data['order'] = counter

            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message":"You do not have permission to perform this action."} )

@permission_classes([IsAuthenticated])
class QuestionDetail(APIView):

    def validate_user(self, request, questionid):
        try:
            question = self.get_question(pk=questionid)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        quiz = Quiz.objects.get(pk = question.quiz_id)
        if quiz.owner_id != request.user.id and not request.user.is_staff:
            raise PermissionDenied()

    def get_question(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, pk):
        question = self.get_question(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = self.get_question(pk)
        self.validate_user(request, pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = self.get_question(pk)
        self.validate_user(request, pk)
        question.delete()
        return Response(status=status.HTTP_200_OK, data={"message":"Question deleted successfully!"})

@permission_classes([IsAuthenticated])
class AnswerList(APIView):
    
    def get(self, request):
        answers = Answer.objects.all()
        if not answers:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            question = Question.objects.get(pk=request.data['question'])
        except Question.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"The question related does not exist"})

        quiz = Quiz.objects.get(pk = question.quiz_id)
        if quiz.owner_id == request.user.id:
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message":"You do not have permission to perform this action."} )

@permission_classes([IsAuthenticated])
class AnswerDetail(APIView):

    def validate_user(self, request, answer_id):
        answer = self.get_answer(answer_id)
        quiz_id =  Question.objects.get(pk = answer.question_id).quiz_id
        quiz = Quiz.objects.get(pk = quiz_id)
        if quiz.owner_id != request.user.id and not request.user.is_staff:
            raise PermissionDenied()
        return answer
    
    def validate_put (self,request, question_id):
        question_put = Question.objects.get(pk = question_id)
        quiz = Quiz.objects.get(pk = question_put.quiz_id)
        if quiz.owner_id != request.user.id:
            raise PermissionDenied()

    def get_answer(self, pk):
        try:
            answer = Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404
        return answer

    def get(self, pk):
        answer = self.get_answer(pk)
        serializer = Answer(answer)
        return Response(serializer.data)

    def put(self, request, pk):
        answer = self.validate_user(request,pk)
        self.validate_put(request, answer.question_id)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        answer = self.get_answer(pk)
        self.validate_user(request,pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   



