from django.db import models

# Create your models here.


class Category(models.Model):
    category_name=models.CharField(max_length=120,unique=True)

    def __str__(self):
        return self.category_name


class Expenses(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    amount=models.IntegerField()
    date=models.DateField(auto_now=True)
    note=models.CharField(max_length=120)
    user=models.CharField(max_length=120)

    def __str__(self):
        return str(self.user+str(self.amount))