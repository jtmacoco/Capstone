import os
from django.core.management.base import BaseCommand
import datetime
import time
import yfinance as yf
from capstone_app.models import Stock
import pandas as pd
from joblib import load
from tensorflow import keras
import datetime
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px 
import numpy as np
from keras.layers import *
from keras.models import *
import tensorflow as tf
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import timedelta
from django.utils.timezone import now
#model = keras.models.load_model('/Users/jtm613/spring23/capstone/Capstone/website/capstone_website/capstone_app/lstm_models/')
#model = keras.models.load_model('/var/www/html/Capstone/website/capstone_website/capstone_app/lstm_models')
#model = keras.models.load_model('/home/pi/Capstone/website/capstone_website/capstone_app/lstm_models')
model = keras.models.load_model('/code/capstone_website/capstone_app/lstm_models')
def get_predicted_price(sid):
    s=yf.Ticker(sid)
    stock=s.history(start="1970-01-01")
    stock_close=stock[['Close']]
    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit_transform(stock_close)
    prev=stock_close[-30:].values
    scale_prev=scaler.transform(prev)
    input=[]
    input.append(scale_prev)
    input=np.array(input)
    input=np.reshape(input,(input.shape[0],input.shape[1],1))
    predicted=model.predict(input)
    predicted=scaler.inverse_transform(predicted)
    return round(float(predicted),2)
def update_stock_prices():
    stocks = Stock.objects.all()
    for stock in stocks:
        stock.closing_price = get_predicted_price(stock.stock_name)
        stock.save()
class Command(BaseCommand):
    help = 'Updates the closing price of stocks'

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        update_stock_prices()
