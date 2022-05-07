from datetime import date
from quizzes_task.tasks.send_email import send_email_task
from .serializers import QuizPerformanceSerializer, QuizTrySerializer
from .models import Question, Answer, Quiz, QuizPerformance, QuizTry
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User


from decimal import Decimal
from datetime import date

@permission_classes([IsAuthenticated])
class QuizTryList(APIView):

    def get(self, request):
        try:
            quiz_tries = QuizTry.objects.filter(owner_id = request.user.id)
        except QuizTry.DoesNotExist:    
            Response(status=status.HTTP_204_NO_CONTENT, data={"message":"There is no quizzes completed!"})
        serializer = QuizTrySerializer(quiz_tries, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            quiz = Quiz.objects.get(pk=request.data['quiz'])
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        quiz_tries =  QuizTry.objects.filter(quiz_id= quiz.id_quiz)
        if not quiz_tries:
            request.data['owner'] = request.user.id
            serializer = QuizTrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if (quiz_tries.last().status ==  'OP'):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"You need to finish the quiz to try again"})
            else:
                request.data['owner'] = request.user.id
                serializer = QuizTrySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class QuizPerformanceList(APIView):

    def get(self, request):
        try:
            quiz_performance = QuizPerformance.objects.filter(owner_id = request.user.id)
        except QuizPerformance.DoesNotExist:
            Response(status=status.HTTP_204_NO_CONTENT, data={"message":"There is not answers submited for any test!"})
        serializer = QuizPerformanceSerializer(quiz_performance, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            quiz_try = QuizTry.objects.get(pk=request.data['quiz_try'], owner= request.user.id)
        except QuizTry.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"You cannot submit in this quiz!"})

        if Quiz.objects.get(pk = quiz_try.quiz_id).status != 'DR':
            next_question = QuizPerformance.objects.filter(quiz_try = quiz_try.id).count() +  1
            if next_question == request.data['question']:
                answer = Answer.objects.get(pk = request.data['answer'])
                if request.data['question'] == answer.question_id:
                    serializer = QuizPerformanceSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"Question does not belong to quiz!"})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"You cannot submit this question!"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"You cannot start drawer quizzes!"})

@permission_classes([IsAuthenticated])
class FinishQuiz(APIView):
    def put(self, request, pk):
        try:
            quiz_try = QuizTry.objects.get(pk=pk, owner= request.user.id)
        except QuizTry.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"You cant perform this action!"})

        if quiz_try.status == 'OP':
            quiz_try.status = 'FN'
            quiz_try.save()
            quiz_performance = QuizPerformance.objects.filter(quiz_try = quiz_try.id)
            score = 0
            if quiz_performance:
                for item in quiz_performance:
                    answer = Answer.objects.get(pk = item.answer_id)
                    if answer.isCorrect:
                        question_score = Question.objects.get(pk = answer.question.id) 
                        score = score + question_score.score 
                quiz_try.score = score
                quiz_try.save()

                email = User.objects.get(pk= request.user.id).email
                quizz_name = Quiz.objects.get(pk = quiz_try.quiz_id).name
                today = date.today().strftime("%d/%m/%Y %H:%M")
                msg = f'''
                    Hello dear user, you have completed the quiz "{quizz_name.capitalize()}" at {today}
                    with a record of {score} points
                '''
                send_email_task.delay(
                    'Quiz completed',
                    msg.strip(),
                   'fmartinezr195@gmail.com'
                )
                return Response(status=status.HTTP_200_OK, data={"message":"Quiz finished successfuly"})
        else:
            Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"Quiz already finished"})

                    







            