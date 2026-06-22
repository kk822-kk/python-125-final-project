from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_comment(value):
    if not value.strip():
        raise ValidationError('კომენტარი არ უნდა იყოს ცარიელი.')
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    shared_from = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='shares')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.created_at:%d/%m/%Y %H:%M}"
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def likes_count(self):
        return self.likes.count()
    
    def is_share(self):
        return self.shared_from is not None
    


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='like') # ახალი ველი!
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)   



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_comment])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.user.username} - პროფილი"
    
