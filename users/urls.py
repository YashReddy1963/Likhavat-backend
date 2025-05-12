from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, LogoutView, UserProfileUpdateView, GetUserProfileView, UserBlogView, BookmarkListCreateView, BookmarkDeleteView, LikeListCreateView, LikeDeleteView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/",LoginView.as_view(), name="login"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("userblog/", UserBlogView.as_view(), name='get-user-blogs'),
    path("profile/", GetUserProfileView.as_view(), name='get-user-profile'),
    path("update-profile/", UserProfileUpdateView.as_view(), name='update-profile'),
    path("bookmarks/", BookmarkListCreateView.as_view(), name="bookmarks"),
    path("bookmarks/<int:blog_id>/", BookmarkDeleteView.as_view(), name="bookmark-delete"),
    path("likes/", LikeListCreateView.as_view(), name="blog-likes"),
    path("likes/<int:blog_id>/", LikeDeleteView.as_view(), name='unlike-blog'),
] 