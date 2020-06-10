from django.db import models

class Question(models.Model):
    question_text = models.Charfield(max_length=255)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.Charfield(max_length=200)
    vote = models.IntegerField(default=0)