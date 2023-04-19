from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User as auth_user
import json
from datetime import date
# Create your models here.
class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    closing_price = models.FloatField()
    def __str__(self):
       return self.stock_name

class Portfolio(models.Model):
    author = models.ForeignKey(auth_user,on_delete=models.CASCADE)
    stocks = models.ForeignKey(Stock,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.author) + " Portfolio: " + str(self.stocks)

class Performance(models.Model):
    name = models.CharField(max_length=255)
    performance_data=models.JSONField()

    def __str__(self):
        return str(self.name) + " Performance " 

    def set_data(self,name,start_date,stock_price_list,predicted_price_list):
        data_dict={
            "name":name,
            "start_date":start_date.isoformat(),
            "stock_price_list":stock_price_list,
            "predicted_price_list":predicted_price_list,
        }
        self.name = name
        self.performance_data = data_dict

    def get_name(self):
        return self.name

    def get_stock_price_list(self):
        data_dict=self.performance_data
        return data_dict['stock_price_list']

    def get_predicted_price_list(self):
        data_dict=self.performance_data
        return data_dict['predicted_price_list']
       
    def get_start_date(self):
        data_dict=self.performance_data
        return date.fromisoformat(data_dict['start_date'])

