import calendar
from datetime import datetime
from django.utils import timezone
from blogs.models import Blogs, BlogView
from django.db.models import Count, F
from django.db.models import Min
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncMonth, TruncDay

# Create your views here.

# blog creation to current date, month list view
class BlogMonthView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        first_blog = Blogs.objects.filter(author=user).aggregate(Min('created_at'))['created_at__min']
        if not first_blog:
            return Response([])
        
        months = []
        current = timezone.now()
        iter_date = first_blog.replace(day=1)

        while iter_date <= current:
            month_str = iter_date.strftime('%Y-%m')
            months.append({
                "label": iter_date.strftime("%B %Y"),
                "value": month_str
            })
            if iter_date.month == 12:
                iter_date = iter_date.replace(year=iter_date.year + 1, month=1)
            else:
                iter_date = iter_date.replace(month=iter_date.month + 1)

        return Response(months)
    
# blog analytics view
class BlogAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        month = request.query_params.get('month')
        year, month = map(int, month.split('-'))

        all_user_blogs = Blogs.objects.filter(author=user)

        # blog views in the selected month
        view_data = BlogView.objects.filter(blog__in=all_user_blogs) \
    .annotate(day=TruncDay('viewed_at')) \
    .values('day') \
    .annotate(view_count=Count('id')) \
    .order_by('day')


        views_over_time = [
            {"date": v["day"].strftime('%Y-%m-%d'), "views": v["view_count"]}
            for v in view_data
        ]

        # blogs created in the selected month for likes chart
        blogs_in_month = all_user_blogs.filter(created_at__year=year, created_at__month=month)

        likes_per_blog = blogs_in_month.annotate(
            like_count=Count('blog_likes')
        ).filter(like_count__gt=0).values("title", "like_count")

        
        # top recent blog this month
        recent_blog = all_user_blogs.order_by('-created_at').first()
        if recent_blog:
            engagement_count = {
                "likes": recent_blog.blog_likes.filter(created_at__year=year, created_at__month=month).count(),
                "comments": recent_blog.comments.filter(created_at__year=year, created_at__month=month).count(),
                "views": BlogView.objects.filter(blog=recent_blog, viewed_at__year=year, viewed_at__month=month).count()
            }
            top_blog = {
                "title": recent_blog.title,
                "data": [
                    {"label": "Likes", "value": engagement_count["likes"]},
                    {"label": "Comments", "value": engagement_count["comments"]},
                    {"label": "Views", "value": engagement_count["views"]}
                ]
            }
        else:
            top_blog = {}
        

        return Response({
            "views_over_time": views_over_time,
            "likes_per_blog": list(likes_per_blog),
            "top_blog": top_blog
        })
