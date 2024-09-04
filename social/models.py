from django.db import models
from account.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from django_resized import ResizedImageField
from datetime import datetime

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    caption = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
    
    def __str__(self) -> str:
        return self.author.first_name
    
    def get_absolute_url(self):
        return reverse('social:post_detail',args=[self.id])
    
class Image(models.Model):
    def get_upload_path(instance, file_name):
        today = datetime.now()
        year = today.year
        return f"{year}/{file_name}"        
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image_file = ResizedImageField(upload_to=get_upload_path, size=[250, 250], quality=75, crop=['middle', 'center'])
    
    def delete(self, *args, **kwargs):
        storage , path = self.img.image_file.storage, self.img.image_file.path 
        storage.delete(path)
        super().delete(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.user.username


