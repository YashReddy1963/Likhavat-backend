from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, LogoutView, UserProfileUpdateView, GetUserProfileView, UserBlogView, BookmarkListCreateView, BookmarkDeleteView, LikeListCreateView, LikeDeleteView, CommentListCreateView, FollowToggleView, UserFollowerCount, IsFollowingView, FollowersListView, FollowingListView

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
    path("blogs/<int:blog_id>/comments/", CommentListCreateView.as_view(), name='comment-list-create'),
    path('follow/<str:user_id>/', FollowToggleView.as_view(), name='toggle-follow'),
    path('follow-count/<str:user_id>/', UserFollowerCount.as_view(), name='follow-count'),
    path('is-following/<str:user_id>/',IsFollowingView.as_view(), name='is-following'),
    path('followers-list/<str:user_id>/', FollowersListView.as_view(), name='followers-list'),
    path('following-list/<str:user_id>/', FollowingListView.as_view(), name='following-list'),
] 