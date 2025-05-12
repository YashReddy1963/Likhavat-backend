from .models import Blogs, Tag
from django.conf import settings
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
    
# Blog creation and updation view
class BlogCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = BlogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        blog = get_object_or_404(Blogs, pk=pk, author=request.user)

        data = request.data

        tag_names = request.data.getlist('tags')
        tag_objs = []

        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            tag_objs.append(tag)

        if tag_objs:
            blog.tags.set(tag_objs)

        cover_image = request.FILES.get('cover_image')
        if cover_image:
            blog.cover_image = cover_image
        
        is_published = request.data.get('is_published')
        if is_published is not None:
            blog.is_published = is_published in ['true', 'True', True]
        
        blog.save()
        serializer = BlogCreateSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Bloglist view for displaying blogs on home page
class BlogListView(ListAPIView):
    queryset = Blogs.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = BlogCreateSerializer

# BlogDetail fetch view to fetch the whole blog content
class BlogDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, blog_id):
        blog = get_object_or_404(Blogs, id=blog_id)
        serializer = BlogCreateSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Image upload view for blog content
class BlogImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'No image provided'}, status=400)
        path = default_storage.save(f'blog_images/{image.name}', image)

        return Response({'url': settings.MEDIA_URL + path})