from django.db import models
from django.contrib.auth import get_user_model

# Create your modprofileels here.

# Blog content model
User = get_user_model()
class Blogs(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.title
    
# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
# Bookmarking blogs model
class Bookmark(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'blog')

# Like blogs model
class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'blog')

# Blog View model to for storing the blogs visited by the user
class BlogView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')

# Notification model
class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('RECOMMENDATION', 'Recommendation'),
        ('NEW_BLOG', 'New Blog'),
        ('NEW_FOLLOWER', 'New Follower'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications") 
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="initiated_notifications")
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(choices=NOTIFICATION_TYPE, max_length=20)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)