from django.urls import path
from .views import BlogImageUploadView, BlogCreateView, BlogListView, BlogDetailView, BlogListAuthorSugView, BlogTTSView, BlogRecommendationView, UserNotificationsView, MarkNotifcationsAsSeenView, UnseenNotificationCountView, WritingAssistantView

urlpatterns = [
    path('all/', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('recommendations/', BlogRecommendationView.as_view(), name='blog-recommendation'),
    path('notifications/', UserNotificationsView.as_view(), name='user-notifications'),
    path('notifications/mark-seen/', MarkNotifcationsAsSeenView.as_view(), name='mark-notifications-seen'),
    path('notifications/unseen-count/', UnseenNotificationCountView.as_view(), name='unseen-notifications-count'),
    path('assistant/', WritingAssistantView.as_view(), name='writing-assistant'),
    path('<int:blog_id>/tts/', BlogTTSView.as_view(), name='blog-tts'),    
    path('update/<int:pk>/', BlogCreateView.as_view(), name='blog-update'),
    path('<str:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('upload-image/', BlogImageUploadView.as_view(), name='upload-image'),
    path('<str:author_id>/blog-sug/', BlogListAuthorSugView.as_view(), name='blog-author-suggestion-view'),
]