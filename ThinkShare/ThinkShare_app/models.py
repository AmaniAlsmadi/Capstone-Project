from django.db import models
from django.contrib.auth.models import User
import markdown
from django.utils.safestring import mark_safe

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='category_image/')

    def __str__(self):
        return self.category_name
    
    
from django.contrib.auth.models import User
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(blank=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def formatted_content(self):
        html_content = markdown.markdown(self.content, extensions=['fenced_code', 'codehilite'])
        return mark_safe(html_content)
    
    def likes_count(self):
        return self.votes.filter(value=1).count()

    def dislikes_count(self):
        return self.votes.filter(value=-1).count()
    
    def liked_by(self, user):
        return self.votes.filter(user=user, value=1).exists()

    def disliked_by(self, user):
        return self.votes.filter(user=user, value=-1).exists()
    
    def __str__(self):
        return self.title

    
class ArticleImages(models.Model):
    image_url = models.ImageField(upload_to='article_image/')
    article = models.ForeignKey(Article,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.image_url)
    

    
class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Vote(models.Model):
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.article.title}: {self.value}"


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article') 

    def __str__(self):
        return f"{self.user.username} → {self.article.title}"
    

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


