from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('benchmark', views.benchmark,name='benchmark_page'),
    path('<str:sid>', views.stocks,name='stocks_pages'),
]