from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Comment, Follow

# User profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
            'name', 'bio', 'email', 'social_links',
            'profile_image', 'banner_image'
        ]
        extra_kwargs = {
            'email': {'required': False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
# User mini serializer for following and followers info
User = get_user_model()
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email','profile_image']
    
# Comments serailizer recursive and comment creation
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    
class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    replies = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment 
        fields = ['id', 'blog', 'user', 'user_name', 'content', 'parent', 'replies', 'created_at']
        read_only_fields = ['user', 'user_name', 'replies', 'created_at']

    def create(self, validated_data):
        request = self.context.get("request")
        blog_id = self.context.get("view").kwargs.get("blog_id")
        validated_data["user"] = request.user
        validated_data["blog_id"] = blog_id

        return Comment.objects.create(**validated_data)
    
# Following serializer
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'followed_at']