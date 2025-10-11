from django.urls import path
from . import views

urlpatterns =[
    path('',views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('article/create/', views.create_article, name='create_article'),
    path('article/<int:pk>/', views.article_details, name='details'),
    path('article/<int:pk>/edit/', views.update_article, name='article_edit'),
    path('article/<int:pk>/delete/', views.delete_article, name='article_delete'),
    path('comment/<int:pk>/edit/', views.update_comment, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='comment_delete'),

]