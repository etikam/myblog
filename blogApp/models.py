from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 150)
    image = models.ImageField(upload_to="category_images", height_field=None, width_field=None, max_length=100)

    

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name

    


class Article(models.Model):
    title = models.CharField(max_length = 150)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='image-blog', height_field=None, width_field=None, max_length=100)
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.title



class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self)->str:
        return f'{self.created_at}'