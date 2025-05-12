from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, LogoutView, UserProfileUpdateView, GetUserProfileView, UserBlogView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/",LoginView.as_view(), name="login"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("userblog/", UserBlogView.as_view(), name='get-user-blogs'),
    path('profile/', GetUserProfileView.as_view(), name='get-user-profile'),
    path("update-profile/", UserProfileUpdateView.as_view(), name='update-profile'),
] 