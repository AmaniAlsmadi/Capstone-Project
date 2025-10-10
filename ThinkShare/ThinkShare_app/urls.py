from django.urls import path
from . import views

urlpatterns =[
    path('',views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('article/create/', views.create_article, name='create_article'),
    path('article/<int:pk>/', views.article_datails, name='details'),

]