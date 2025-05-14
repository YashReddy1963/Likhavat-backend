from gtts import gTTS
from django.conf import settings
from rest_framework import status
from django.shortcuts import render
from django.utils.html import strip_tags
from .models import Blogs, Tag, BlogView, Notification
from rest_framework.response import Response
from rest_framework.views import APIView, View
from django.http import FileResponse, Http404
from .serializers import BlogCreateSerializer, NotificationSerializer
from django.shortcuts import get_object_or_404
from .recommendations.utils import get_blog_recommendations
from rest_framework.generics import ListAPIView, RetrieveAPIView
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

# Blogs realted to particular author suggestion view
class BlogListAuthorSugView(ListAPIView):
    permission_classes = [AllowAny]
    def get(self,request, author_id):
        blogs = Blogs.objects.filter(author=author_id,is_published=True).order_by("-created_at")
        serializer = BlogCreateSerializer(blogs, many=True)
        return Response(serializer.data)

# BlogDetail fetch view to fetch the whole blog content
class BlogDetailView(RetrieveAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogCreateSerializer
    permission_classes = [AllowAny]

    def get(self,reqest, blog_id):
        blog = get_object_or_404(Blogs, id=blog_id)
        serializer = BlogCreateSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            BlogView.objects.get_or_create(user=request.user, blog=instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# Image upload view for blog content
class BlogImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'No image provided'}, status=400)
        path = default_storage.save(f'blog_images/{image.name}', image)

        return Response({'url': settings.MEDIA_URL + path})
    
# View to create/fetch blog text into audio
class BlogTTSView(View):
    def get(self, request, blog_id):
        try:
            blog = Blogs.objects.get(id=blog_id)
        except Blogs.DoesNotExist:
            raise Http404("Blog not found")
        
        audio_dir = settings.MEDIA_ROOT / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        file_path = audio_dir / f"tss_blog_{blog_id}.mp3"

        if not file_path.exists():
            plain_text = strip_tags(blog.content)
            tts = gTTS(text=plain_text, lang='en')
            tts.save(str(file_path))

        return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
    
# View to recommend blogs according to user interest
class BlogRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        all_blogs = Blogs.objects.all()
        liked_blogs = Blogs.objects.filter(like__author=user)
        viewed_blogs = Blogs.objects.filter(blogview__user=user)

        recommend_ids = get_blog_recommendations(user, all_blogs, liked_blogs, viewed_blogs)
        recommend = Blogs.objects.filter(id__in=recommend_ids)

        serializer = BlogCreateSerializer(recommend, many=True)
        return Response(serializer.data)
    
# View to get new notifications
class UserNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
# To mark notification is seen or not
class MarkNotifcationsAsSeenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.notifications.filter(seen=False).update(seen=True)
        return Response({'message': 'Notifications marked as seen'})
    
# To Count unseen notifications
class UnseenNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = request.user.notifications.filter(seen=False).count()
        return Response({'count': count})
