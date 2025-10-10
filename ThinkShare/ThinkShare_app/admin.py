from django.contrib import admin
from .models import Article, Categories

admin.site.register(Categories)
admin.site.register(Article)
