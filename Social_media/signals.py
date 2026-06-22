from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Notification, Comment, Post

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        if instance.post.author != instance.author:
            Notification.objects.create(
                recipient=instance.post.author,
                sender=instance.author,
                post=instance,
                notification_type='comment'
            )

@receiver(m2m_changed, sender=Post.likes.through)
def create_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user_who_liked = User.objects.get(pk=user_id)
            if instance.author != user_who_liked:
                already_exists = Notification.objects.filter(
                    recipient=instance.author,
                    sender=user_who_liked,
                    post=instance,
                    notification_type='like'
                ).exists()
                if not already_exists:
                    Notification.objects.create(
                        recipient=instance.author,
                        sender=user_who_liked,
                        post=instance,
                        notification_type='like'
                    )