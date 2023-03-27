import json
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import requests
import urllib.request
import urllib3
from . forms import RegisterForm
from . forms import StocksForm
from django.contrib.auth import login, logout, authenticate
import pandas as pd
import yfinance as yf
from joblib import load
from tensorflow import keras
#impoprt libraries used
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px 
import numpy as np
from keras.layers import *
from keras.models import *
import tensorflow as tf
model=keras.models.load_model('capstone_app/models')
# Create your views here.
def home(request):
    if request.method =='POST':
        form=StocksForm(request.POST)
        if form.is_valid():
            stock = request.POST['stock']
            return HttpResponseRedirect(stock)
    else:
        form=StocksForm()
    #return render(request,'main/home.html')
    return render(request,'main/home.html',{'form':form})

def stocks(request,sid):
    if request.method =='POST':
        form=StocksForm(request.POST)
        if form.is_valid():
            stock = request.POST['stock']
            return HttpResponseRedirect(stock)
    else:
        form=StocksForm()
    s=yf.Ticker(sid)
    stock=s.history(start="1970-01-01")
    stock_close=stock[['Close']]
    open_close=stock[['Open','Close']]
    graph=px.line(open_close,x=open_close.index,y=open_close.columns[:])
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
    context={}
    context['stocks']=sid
    context['predict']=round(float(predicted),2)
    context['graph']=graph.to_html()
    context['form']=form
    return render(request,'main/stocks.html',context)

def benchmark(request):
    return render(request,'main/benchmark.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('/home')

    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html',{"form":form})
