from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import OTP, User, Comment, Follow
from blogs.models import Blogs, Bookmark, Like
from django.shortcuts import get_object_or_404
from blogs.serializers import BlogCreateSerializer, BookMarkSerializer, LikedBlogSerizlizer
from .serializers import UserProfileSerializer, CommentSerializer, UserMiniSerializer
import random

# Create your views here.

# Registration view
class RegisterView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([name, email, password]):
            return Response({"detail":"All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(email=email, password=password, name=name)
        user.is_verified = False
        user.save()

        otp_code = f"{random.randint(100000, 999999)}"
        OTP.objects.create(name=user, otp=otp_code)

        send_mail(
            subject="Verify your email",
            message=f"Your OTP is: {otp_code}",
            from_email="yashmunurreddy63@gmail.com",
            recipient_list=[email],
        )

        return Response({"detail": "OTP sent to your email."}, status=status.HTTP_200_OK)
    
# VerifyOTP view
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"detail": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp_record = OTP.objects.filter(name=user).latest("created_at")
        except OTP.DoesNotExist:
            return Response({"detail": "OTP not found."}, status=status.HTTP_404_NOT_FOUND)

        if otp_record.is_expired():
            return Response({"detail": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.otp != otp:
            return Response({"detail": "Incorrect OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()

        return Response({"detail": "Account verified successfully!"}, status=status.HTTP_200_OK)
    
# Login view
User = get_user_model()
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail":"Email or password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token),"refresh": str(refresh), "detail":"Login Successful!"},status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# User profile view
class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

# User profile update view
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Bloglist view of blogs created by the user itself
class UserBlogView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        blogs = Blogs.objects.filter(author=user,is_published=True).order_by("-created_at")
        serializer = BlogCreateSerializer(blogs, many=True)
        return Response(serializer.data)
    
# Bookmarked blogs list view to list out saved blogs
class BookmarkListCreateView(generics.ListCreateAPIView):
    serializer_class = BookMarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(author=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Delete bookmarked blogs
class BookmarkDeleteView(generics.DestroyAPIView):
    serializer_class = BookMarkSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Bookmark.objects.get(author=self.request.user, blog=self.kwargs['blog_id'])
    
# Liked blogs list view to list out liked blogs
class LikeListCreateView(generics.ListCreateAPIView):
    serializer_class = LikedBlogSerizlizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(author=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Unlike liked blogs
class LikeDeleteView(generics.DestroyAPIView):
    serializer_class = LikedBlogSerizlizer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Like.objects.get(author=self.request.user, blog=self.kwargs['blog_id'])

# Comments creation and fetching comment content
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return Comment.objects.filter(blog_id=blog_id, parent=None).order_by('-created_at')
    
    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_id']
        serializer.save(user=self.request.user, blog_id=blog_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "request": self.request,
            "view": self,
        })
        return context
    
# FollowToggle view to follow and unfollow the user
class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        current_user = request.user

        if user_to_follow == current_user:
            return Response({'error': 'You cannot follow yourself'}, status=400)
        
        follow, created = Follow.objects.get_or_create(follower=current_user, following=user_to_follow)

        if not created:
            follow.delete()
            return Response({'message': 'Unfollowed'}, status=200)
        
        return Response({'message': 'Followed'}, status=201)

# View to get follower-following of current user
class UserFollowerCount(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        followers = user.followers.count()
        following = user.following.count()
        
        return Response({'followers': followers, 'following': following})
    
# View to check current user already follows the profile user or not
class IsFollowingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()
        
        return Response({'is_following': is_following})
    
# View to get info of followers
class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        followers = Follow.objects.filter(following_id=user_id).select_related('follower')
        serializer = UserMiniSerializer([f.follower for f in followers], many=True)
        return Response(serializer.data)
    
# View to get info of followings
class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        following = Follow.objects.filter(follower_id=user_id).select_related('following')
        serializer = UserMiniSerializer([f.following for f in following], many='True')
        return Response(serializer.data)
