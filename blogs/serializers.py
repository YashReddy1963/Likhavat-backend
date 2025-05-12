from rest_framework import serializers
from .models import Blogs, Tag, Bookmark, Like

# blogs serializer
class BlogCreateSerializer(serializers.ModelSerializer):
    author_image = serializers.ImageField(source='author.profile_image', read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    cover_image = serializers.ImageField(use_url=True, required=False, allow_null=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
        required=False,
        allow_null=True
    )
    class Meta:
        model = Blogs
        fields = '__all__'
        read_only_fields = ['author', 'create_at', 'updated_at']

# bookmark serializer
class BookMarkSerializer(serializers.ModelSerializer):
    blog_data = BlogCreateSerializer(source='blog', read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id','blog','bookmarked_at','blog_data']
    
# likedBlog serializer
class LikedBlogSerizlizer(serializers.ModelSerializer):
    blog_data = BlogCreateSerializer(source='blog', read_only=True)
    class Meta:
        model = Like
        fields = ['id','blog','created_at','blog_data']