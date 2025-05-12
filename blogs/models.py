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