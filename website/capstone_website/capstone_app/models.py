from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User as auth_user
# Create your models here.
class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    closing_price = models.FloatField()
    def __str__(self):
       return self.stock_name

class Portfolio(models.Model):
    author = models.ForeignKey(auth_user,on_delete=models.CASCADE)
    stocks = models.OneToOneField(Stock,on_delete=models.CASCADE)
    class Meta:
        unique_together = [['author','stocks']]
    def __str__(self):
        return str(self.author) + " Portfolio: " + str(self.stocks)