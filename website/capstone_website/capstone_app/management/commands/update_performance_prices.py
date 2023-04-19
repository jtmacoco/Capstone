import json
from datetime import datetime, time
from django.core.management.base import BaseCommand
from capstone_app.models import Performance
from capstone_app.models import Portfolio
import yfinance as yf
def get_update_predicted():
    portfolio_objects=Portfolio.objects.all()
    performance={}
    for portfolio in portfolio_objects:
        performance.setdefault(str(portfolio.author), 0)
        performance[str(portfolio.author)]+=portfolio.stocks.closing_price
    return performance

def get_update_stocks():
    portfolio_objects=Portfolio.objects.all()
    performance={}
    for portfolio in portfolio_objects:
        performance.setdefault(str(portfolio.author), 0)
        stock=portfolio.stocks.stock_name
        stock_data=yf.Ticker(stock)
        stock_history = stock_data.history(period='1d')
        performance[str(portfolio.author)]+=round(float(stock_history['Close'].iloc[-1]),2)
    return performance

class Command(BaseCommand):
    help = 'Updates stock_price_list and predicted_price_list in Performance model'
    def handle(self, *args, **options):
        predicted_dict=get_update_predicted()
        stock_dict=get_update_stocks()
        performance_keys=list(predicted_dict)
        now = datetime.now()
        performances = Performance.objects.all()
        for performance in performances:
            stock_price_list = performance.performance_data.get('stock_price_list', [])
            predicted_price_list = performance.performance_data.get('predicted_price_list', [])
            if performance.get_name() in performance_keys:
                stock_price_list.append(stock_dict[performance.get_name()])
                predicted_price_list.append(predicted_dict[performance.get_name()])

            performance.performance_data['stock_price_list'] = stock_price_list
            performance.performance_data['predicted_price_list'] = predicted_price_list
            performance.save()
        self.stdout.write(self.style.SUCCESS('Stock price and predicted price updated successfully.'))

