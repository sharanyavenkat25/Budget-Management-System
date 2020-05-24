from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ExpenseInfo(models.Model):
    expense_name = models.CharField(max_length=20)
    cost = models.FloatField()
    date_added = models.DateField()
    user_expense = models.ForeignKey(User, on_delete=models.CASCADE)