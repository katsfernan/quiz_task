from quiz_app.models import Quiz, Answer, Question
from django.conf import settings
from django.db import models


class QuizTry (models.Model):
    TRY_STATUSES=(
        ('OP','On progress'),
        ('FN','Finished')
    )

    score = models.IntegerField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length = 2, choices=TRY_STATUSES, default=TRY_STATUSES[0][0])
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_quiztry")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='owner_qt_id', on_delete=models.CASCADE, related_name='owner_try')


class QuizPerformance(models.Model):
    quiz_try = models.ForeignKey(QuizTry,  on_delete=models.CASCADE, related_name="quiz_try_perf")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='owner_qp_id', on_delete=models.CASCADE, related_name='owner_perf')
    question = models.ForeignKey(Question,  on_delete=models.CASCADE, related_name="question_perf")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_perf")
     