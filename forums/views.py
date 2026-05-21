from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from .models import Forum

def home(request):
    """Trang chủ: danh sách chuyên mục + thống kê (bảng 2.2)"""
    from topics.models import Topic
    from accounts.models import User
    forums      = Forum.objects.filter(is_active=True)
    hot_topics  = Topic.objects.filter(
                    forum__is_active=True
                  ).order_by('-view_count')[:5]
    stats = {
        'total_users':  User.objects.count(),
        'total_topics': Topic.objects.count(),
        'total_forums': forums.count(),
    }
    return render(request, 'forums/home.html', {
        'forums':     forums,
        'hot_topics': hot_topics,
        'stats':      stats,
    })
from django.core.exceptions import PermissionDenied
from django.contrib import messages

def create_forum(request):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        raise PermissionDenied
    if request.method == 'POST':
        name = request.POST.get('forum_name', '').strip()
        desc = request.POST.get('description', '').strip()
        if not name:
            messages.error(request, 'Tên chuyên mục không được để trống.')
        elif Forum.objects.filter(forum_name=name).exists():
            messages.error(request, 'Tên chuyên mục đã tồn tại.')
        else:
            Forum.objects.create(
                forum_name=name,
                description=desc,
                created_by=request.user,
                is_active=True
            )
            messages.success(request, f'Đã tạo chuyên mục "{name}".')
            return redirect('home')
    return render(request, 'forums/create_forum.html')