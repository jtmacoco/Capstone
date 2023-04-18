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
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px 
import numpy as np
from keras.layers import *
from keras.models import *
import tensorflow as tf
from . import models
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import timedelta
from django.utils.timezone import now
import asyncio
from functools import lru_cache

model=keras.models.load_model('capstone_app/lstm_models')
# Create your views here.
def home(request):
    sid = '^GSPC'
    predicted_price=get_predicted_price('^GSPC')
    graph=get_graph('^GSPC')
    if 'Submit' in request.POST:
        form=StocksForm(request.POST)
        if form.is_valid():
            stock = request.POST['stock']
            tick=yf.Ticker(stock)
            if not check_stock_symbol(stock):
                messages.error(request, 'Stock does not exist')
                return redirect('/home')
            else:
                return HttpResponseRedirect(stock)
    else:
        form=StocksForm()
    if 'add to portfolio' in request.POST:
        stock_data = models.Stock.objects.filter(stock_name=sid)
        if stock_data.exists() == False:
            stock_data = models.Stock(stock_name=sid.upper(),closing_price=predicted_price)
            stock_data.save()
        else:
            stock_data=models.Stock.objects.get(stock_name=sid)
        portfolio = models.Portfolio.objects.filter(author=request.user, stocks = stock_data)
        if portfolio.exists() == False:
            portfolio = models.Portfolio(author=request.user,stocks=stock_data)
            portfolio.save()
    try:
        company_name = get_company_name("^GSPC")
    except:
        company_name="Stock Name not found"
    context={}
    context['stocks']='^GSPC'
    context['company_name']=company_name
    context['predict']=round(float(predicted_price),2)
    context['graph']=graph.to_html()
    context['form']=form
    #return render(request,'main/home.html')
    return render(request,'main/home.html',context)

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
    sid=sid.upper()
    if not check_stock_symbol(sid):
        messages.error(request, 'Stock does not exist')
        return redirect(request.META.get('HTTP_REFERER'))
    if 'Submit' in request.POST:
        form=StocksForm(request.POST)
        if form.is_valid():
            stock = request.POST['stock']
            return HttpResponseRedirect(stock)
    else:
        form=StocksForm()
    predicted_price=get_predicted_price(sid)
    graph=get_graph(sid)
    cur_user=request.user
    if 'add to portfolio' in request.POST:
        stock_data = models.Stock.objects.filter(stock_name=sid)
        if stock_data.exists() == False:
            stock_data = models.Stock(stock_name=sid.upper(),closing_price=predicted_price)
            stock_data.save()
        else:
            stock_data=models.Stock.objects.get(stock_name=sid)
        portfolio = models.Portfolio.objects.filter(author=request.user, stocks = stock_data)
        if portfolio.exists() == False:
            portfolio = models.Portfolio(author=request.user,stocks=stock_data)
            portfolio.save()
    try:
        company_name = get_company_name(sid)
    except:
        company_name="Stock Name not found"
    context={}
    context['stocks']=sid.upper()
    context['company_name']=company_name
    context['predict']=round(float(predicted_price),2)
    context['graph']=graph.to_html()
    context['form']=form
    return render(request,'main/stocks.html',context)

API_KEY = "MO4HBDRDZNNUGH79 "
def get_company_name(symbol):
    if symbol.upper()== "^GSPC":
        company_name="S&P 500"
        return company_name
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=API_KEY'
    response = requests.get(url)
    data = response.json()
    company_name = data['Name']
    return company_name

REQUESTS_TIMEOUT = 5

@lru_cache(maxsize=128)
def get_api_data(symbol):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey=API_KEY"
    response = requests.get(url, timeout=REQUESTS_TIMEOUT)
    return response.json()

def check_stock_symbol(symbol):
    if symbol.lower() == "^gspc" or symbol.lower() == "^ixic" or symbol.lower() == "favicon.ico":
        return True
    data = get_api_data(symbol)

    if "bestMatches" in data:
        matches = data["bestMatches"]
        if len(matches) > 0:
            for match in matches:
                if match["1. symbol"].lower() == symbol.lower():
                    return True
    return False

def check_duplicates(sid,user_name):
    portfolio_objects=models.Portfolio.objects.all()
    for p_object in portfolio_objects:
        if p_object.author == user_name and p_object.stocks.stock_name == sid:
            return True
        else:
            return False

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
            login(request)
            return redirect('/login/')

    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html',{"form":form})

def edit_portfolio(request):
    portfolio_objects=models.Portfolio.objects.all()
    cur_user=request.user
    portfolio_dict={}
    p_id = -1
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

def performance(request):
    return render(request,"main/performance.html")
#/Users/jtm613/spring23/capstone/Capstone/website/my_venv/bin/python
#/Users/jtm613/spring23/capstone/Capstone/website/capstone_website/manage.py
