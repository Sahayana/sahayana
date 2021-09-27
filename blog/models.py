
from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.

class MainCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=1100, db_index=True, unique=True)    

    class Meta:
        ordering = ['name']
        verbose_name = 'main category'
        verbose_name_plural = 'main categories'
    
    def __str__(self):
        return self.name    


class Category(models.Model):

    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null= True)
    name = models.CharField(max_length=100, db_index= True, unique= True)
    description = models.TextField()
    slug = models.SlugField(max_length=100, db_index= True, unique= True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:post_in_category', args=[self.main_category.slug, self.slug])
    

class Post(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True)    
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    display = models.BooleanField('Display', default=True)
    recommend = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, null= True) # 추천 기능

    def __str__(self):
        return self.title

    def get_absoulute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_authors')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null= True)
    recommend = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, null= True, related_name='commend_recommends') # 추천 기능


