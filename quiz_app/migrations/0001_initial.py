# Generated by Django 4.0.4 on 2022-05-07 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id_quiz', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('max_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('max_time_to_solve', models.DurationField()),
                ('question_quantity', models.SmallIntegerField(blank=True, null=True)),
                ('image', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=2)),
                ('owner', models.ForeignKey(db_column='owner_id', on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=50, null=True)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz_app.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=50, null=True)),
                ('isCorrect', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz_app.question')),
            ],
        ),
    ]
