from django.db import models
from django.utils import timezone

class condPost(models.Model):
    name = models.CharField(max_length=25, default='namedef')
    field = models.CharField(max_length=25)
    oper = models.CharField(max_length=2)
    valuetext = models.CharField(max_length=25)
    created_date = models.DateTimeField(
            default=timezone.now)
    audusr = models.CharField(max_length=10,default='learners')

    def __str__(self):
        return self.name

class rulePost(models.Model):
    ruletext = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    audusr = models.CharField(max_length=10)
    ruleInt = models.IntegerField()
    comments = models.CharField(max_length=200, default="Initial configuration")

    def publish(self):
        self.save()

    def __str__(self):
        return self.ruletext