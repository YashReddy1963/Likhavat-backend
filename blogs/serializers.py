from rest_framework import serializers
from .models import Blogs, Tag, Bookmark, Like, Notification

# blogs serializer
class BlogCreateSerializer(serializers.ModelSerializer):
    author_socials = serializers.JSONField(source='author.social_links', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    author_banner = serializers.ImageField(source='author.banner_image', read_only=True)
    author_about = serializers.CharField(source='author.bio', read_only=True)
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

# notification serializer
class NotificationSerializer(serializers.ModelSerializer):
    blog_title = serializers.SerializerMethodField()
    blog_id = serializers.SerializerMethodField()
    blog_cover_image = serializers.SerializerMethodField()
    initiator_name = serializers.SerializerMethodField()
    initiator_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'is_read', 'created_at',
            'blog_title', 'blog_id', 'blog_cover_image',
            'initiator_name', 'initiator_profile_image'
        ]

    def get_blog_title(self, obj):
        return obj.blog.title if obj.blog else None

    def get_blog_id(self, obj):
        return obj.blog.id if obj.blog else None

    def get_blog_cover_image(self, obj):
        return obj.blog.cover_image.url if obj.blog and obj.blog.cover_image else None

    def get_initiator_name(self, obj):
        return obj.initiator.name if obj.initiator else None

    def get_initiator_profile_image(self, obj):
        return obj.initiator.profile_image.url if obj.initiator and obj.initiator.profile_image else None

        
