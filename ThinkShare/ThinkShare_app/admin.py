from django.contrib import admin
from .models import Article, Categories,ArticleImages, Comment, Vote, BookMark, Contact 

admin.site.register(Categories)
admin.site.register(Article)
admin.site.register(ArticleImages)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(BookMark)
admin.site.register(Contact)
