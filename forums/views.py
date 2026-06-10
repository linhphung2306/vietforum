from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Forum


def home(request):
    """Trang chủ: danh sách chuyên mục + thống kê"""
    from topics.models import Topic
    from accounts.models import User
    forums     = Forum.objects.filter(is_active=True, is_approved=True)
    hot_topics = Topic.objects.filter(
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


@login_required
def create_forum(request):
    """Mọi user đã đăng nhập đều tạo được — chờ admin duyệt."""
    if request.method == 'POST':
        name = request.POST.get('forum_name', '').strip()
        desc = request.POST.get('description', '').strip()
        if not name:
            messages.error(request, 'Tên chuyên mục không được để trống.')
        elif Forum.objects.filter(forum_name=name).exists():
            messages.error(request, 'Tên chuyên mục đã tồn tại.')
        else:
            # Admin tạo thì duyệt luôn, user thường chờ duyệt
            is_approved = request.user.is_staff
            Forum.objects.create(
                forum_name=name,
                description=desc,
                created_by=request.user,
                is_active=True,
                is_approved=is_approved,
            )
            if is_approved:
                messages.success(request, f'Đã tạo chuyên mục "{name}".')
            else:
                messages.info(request, f'Chuyên mục "{name}" đang chờ admin duyệt.')
            return redirect('forums:home')
    return render(request, 'forums/create_forum.html')


@login_required
def delete_forum(request, forum_id):
    """Chỉ admin/staff mới xóa được chuyên mục."""
    if not request.user.is_staff:
        raise PermissionDenied
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        name = forum.forum_name
        forum.delete()
        messages.success(request, f'Đã xóa chuyên mục "{name}".')
        return redirect('forums:home')
    return render(request, 'forums/confirm_delete_forum.html', {'forum': forum})


@login_required
def approve_forum(request, forum_id):
    """Admin duyệt chuyên mục do user tạo."""
    if not request.user.is_staff:
        raise PermissionDenied
    forum = get_object_or_404(Forum, id=forum_id)
    forum.is_approved = True
    forum.save()
    messages.success(request, f'Đã duyệt chuyên mục "{forum.forum_name}".')
    return redirect('forums:pending_forums')


@login_required
def pending_forums(request):
    """Danh sách chuyên mục chờ duyệt — chỉ admin thấy."""
    if not request.user.is_staff:
        raise PermissionDenied
    forums = Forum.objects.filter(is_approved=False, is_active=True)
    return render(request, 'forums/pending_forums.html', {'forums': forums})