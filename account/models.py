from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='users_images/', null=True, blank=True)
    following = models.ManyToManyField('self', through='Contact', related_name="followers", symmetrical=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.username
    
    def get_followings(self):
        return [contact.user_to for contact in self.rel_from_set.all().order_by('-created')]
    
    def get_followers(self):
        return [contact.user_from for contact in self.rel_to_set.all().order_by('-created')]
    
    def get_absolute_url(self):
        return reverse('account:user_detail', args=[self.username])

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"

