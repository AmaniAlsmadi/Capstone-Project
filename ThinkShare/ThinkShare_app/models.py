from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='category_image/')

    def __str__(self):
        return self.category_name
    
    
class Article(models.Model):
    title = models.CharField(max_length=300)
    content = models.CharField(max_length=3000)
    link = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
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
    Value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return str(self.Value)




