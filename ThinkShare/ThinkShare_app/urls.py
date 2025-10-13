from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('',views.home, name='home'),
    path('articles/', views.articles, name='articles'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('bookmark/', views.bookmark_view, name='bookmark'),
    path('article/create/', views.create_article, name='create_article'),
    path('article/<int:pk>/', views.article_details, name='details'),
    path('article/<int:pk>/edit/', views.update_article, name='article_edit'),
    path('article/<int:article_id>/image/<int:pk>/delete/', views.delete_article_image, name='image_delete'),
    path('article/<int:pk>/delete/', views.delete_article, name='article_delete'),
    path('comment/<int:pk>/edit/', views.update_comment, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='comment_delete'),
    path('bookmark/<int:article_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmark/list/toggle/<int:article_id>/', views.togglelist_bookmark, name='togglelist_bookmark'),

]


