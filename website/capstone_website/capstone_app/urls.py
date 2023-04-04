from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('benchmark', views.benchmark,name='benchmark_page'),
    path('home',views.home,name='home'),
    path('edit_portfolio',views.edit_portfolio,name='edit_portfolio'),
    path('portfolio',views.portfolio,name='portfolio'),
    path('<str:sid>', views.stocks,name='stocks_pages'),
]