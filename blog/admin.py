from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Post, Category, Comment, UserProfile, Rating

@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Get statistics
            context['total_posts'] = Post.objects.count()
            context['total_users'] = User.objects.count()
            context['total_comments'] = Comment.objects.count()
            context['total_categories'] = Category.objects.count()
            
            # Get recent posts
            context['recent_posts'] = Post.objects.all().order_by('-created_at')[:5]
            
            # Get recent activity
            recent_activity = []
            
            # Recent posts
            for post in Post.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)):
                recent_activity.append({
                    'icon': 'file-alt',
                    'description': f'New post created: {post.title}',
                    'time': post.created_at.strftime('%b %d, %Y %H:%M')
                })
            
            # Recent comments
            for comment in Comment.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)):
                recent_activity.append({
                    'icon': 'comment',
                    'description': f'New comment on {comment.post.title}',
                    'time': comment.created_at.strftime('%b %d, %Y %H:%M')
                })
            
            # Recent ratings
            for rating in Rating.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)):
                recent_activity.append({
                    'icon': 'star',
                    'description': f'New rating ({rating.value} stars) on {rating.post.title}',
                    'time': rating.created_at.strftime('%b %d, %Y %H:%M')
                })
            
            # Sort activity by time
            context['recent_activity'] = sorted(recent_activity, key=lambda x: x['time'], reverse=True)[:10]
            
        except Exception as e:
            # Handle any errors gracefully
            context['error'] = str(e)
            context['total_posts'] = 0
            context['total_users'] = 0
            context['total_comments'] = 0
            context['total_categories'] = 0
            context['recent_posts'] = []
            context['recent_activity'] = []
        
        return context

# Register your models here
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Rating)

# Add the dashboard to the admin index
admin.site.index_template = 'admin/dashboard.html'
