from django.conf import settings
from django.db import models

class Quiz (models.Model):
    QUIZ_STATUSES = (
        ('DR', 'Draft'),
        ('PB', 'Published')
    )
    id_quiz = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    max_score = models.DecimalField(max_digits=5,decimal_places=2, null = True, blank=True)
    max_time_to_solve = models.DurationField()
    question_quantity = models.SmallIntegerField(null = True, blank=True)
    image = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=2, choices=QUIZ_STATUSES, default=QUIZ_STATUSES[0][0])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='owner_id', on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self) -> str:
        return f"Quiz related to {self.name}"

class Question (models.Model):
    text = models.CharField(max_length=200)
    image = models.CharField(max_length = 50, null = True)
    score = models.DecimalField(max_digits=5,decimal_places=2)
    order = models.IntegerField(null=True, blank=True)
    quiz = models.ForeignKey(Quiz,related_name='questions', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Question number {self.order} is '{self.text}'"

class Answer(models.Model):
    text = models.CharField(max_length=50)
    image = models.CharField(max_length=50, null=True)
    isCorrect = models.BooleanField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Answer {self.text} is {'correct' if self.isCorrect else 'incorrect'}"




