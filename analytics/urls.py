from django.urls import path
from .views import BlogMonthView, BlogAnalyticsAPIView

urlpatterns = [
    path('blog-months/', BlogMonthView.as_view(), name='blog-month'),
    path('blog-analytics/', BlogAnalyticsAPIView.as_view(), name='blog-analytics'),
]