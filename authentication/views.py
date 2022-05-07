from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from quizzes_task.tasks.send_email import send_email_task
from django.contrib.auth.models import User

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = User.objects.get(email= request.data['email']).email

        msg = f"""
        Hello dear user, you have register successfuly on our site Quiz Tasks!.
         """
        send_email_task.delay(
            'Register site Quiz Tasks',
             msg.strip(),
             email
        )
        return Response(serializer.data)

# class BlacklistTokenUpdateView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = ()

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
