from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Blogs
from users.models import Follow
from .recommendations.utils import get_blog_recommendations

# to notify about new blogs to whom current user follows
@receiver(post_save, sender=Blogs)
def notify_folllowers_on_new_blog(sender, instance, created, **kwargs):
    if created:
        followers = Follow.objects.filter(following=instance.author).values_list('follower', flat=True)
        for user_id in followers:
            Notification.objects.create(
                user_id=user_id,
                blog=instance,
                type='NEW_BLOG'
            )

# to notify about new followers of the current user
@receiver(post_save, sender=Follow)
def notify_on_new_follower(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.following, 
            initiator=instance.follower, 
            type='NEW_FOLLOWER'
        )
 