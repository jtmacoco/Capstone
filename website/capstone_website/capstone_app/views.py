from gc import get_objects
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import requests
import urllib.request
from django.contrib.auth import get_user_model
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
from . import models
from django.contrib.auth.models import User
model=keras.models.load_model('capstone_app/lstm_models')
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

def portfolio(request):
    portfolio_objects=models.Portfolio.objects.all()
    stock_obj=models.Portfolio.stocks
    cur_user=request.user
    portfolio_dict={}
    for p_object in portfolio_objects:
        if cur_user==p_object.author:
            portfolio_dict[p_object.stocks.stock_name]=p_object.stocks.closing_price
    context={}
    context['stock_data']=portfolio_dict
    return render(request,'main/portfolio.html',context)

def stocks(request,sid):
    sid.upper()
    if 'Submit' in request.POST:
        form=StocksForm(request.POST)
        if form.is_valid():
            stock = request.POST['stock']
            return HttpResponseRedirect(stock)
    else:
        form=StocksForm()
    predicted_price=get_predicted_price(sid)
    graph=get_graph(sid)
    if 'add to portfolio' in request.POST:
        stock_data = models.Stock(stock_name=sid.upper(),closing_price=predicted_price)
        stock_data.save()
        portfolio = models.Portfolio(author=request.user,stocks=stock_data)
        portfolio.save()
    context={}
    context['stocks']=sid.upper()
    context['predict']=round(float(predicted_price),2)
    context['graph']=graph.to_html()
    context['form']=form
    return render(request,'main/stocks.html',context)

def get_graph(sid):
    s=yf.Ticker(sid)
    stock=s.history(start="1970-01-01")
    open_close=stock[['Open','Close']]
    graph=px.line(open_close,x=open_close.index,y=open_close.columns[:]) 
    return graph

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

def benchmark(request):
    rmse=2.704493284395157
    test_context={}
    test_context['rmse']=rmse
    return render(request,'main/benchmark.html',test_context)

def login(request):
    return render(request,'registration/login.html')

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

def edit_portfolio(request):
    portfolio_objects=models.Portfolio.objects.all()
    cur_user=request.user
    portfolio_dict={}
    for p_object in portfolio_objects:
        if cur_user==p_object.author:
            portfolio_dict[p_object.stocks.stock_name]=p_object.stocks.closing_price
            p_id=p_object.id
    context={}
    context['stock_data']=portfolio_dict
    context['p_id']=p_id
    return render (request,'main/edit_portfolio.html',context)

def delete_stock(request,sid):
    portfolio_objects=models.Portfolio.objects.all()
    cur_user = request.user
    for p_object in portfolio_objects:
        if cur_user == p_object.author and sid == p_object.stocks.stock_name:
            port_id = p_object.id
    stock=models.Portfolio.objects.get(pk=port_id)
    stock.delete()
    return redirect('edit_portfolio')