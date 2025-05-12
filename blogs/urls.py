from django.urls import path
from .views import BlogImageUploadView, BlogCreateView, BlogListView, BlogDetailView

urlpatterns = [
    path('all/', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('update/<int:pk>/', BlogCreateView.as_view(), name='blog-update'),
    path('<str:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('upload-image/', BlogImageUploadView.as_view(), name='upload-image'),
]