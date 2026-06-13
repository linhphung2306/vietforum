from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from topics.models import Topic, Post
from interactions.models import Report
from accounts.models import User
from forums.models import Forum
from .decorators import moderator_required
from notifications.models import Notification


@moderator_required
def dashboard(request):
    pending_reports = Report.objects.filter(status='pending') \
                            .select_related('post', 'reporter',
                                            'post__author', 'post__topic')
    locked_topics  = Topic.objects.filter(is_locked=True).count()
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_users      = User.objects.filter(date_joined__gte=seven_days_ago).count()
    new_topics     = Topic.objects.filter(created_at__gte=seven_days_ago).count()
    return render(request, 'moderation/dashboard.html', {
        'pending_reports': pending_reports,
        'locked_topics':   locked_topics,
        'new_users':       new_users,
        'new_topics':      new_topics,
    })


@moderator_required
def handle_report(request, report_id):
    """Xử lý báo cáo vi phạm — cập nhật reviewed_by, resolved_at"""
    report = get_object_or_404(Report, id=report_id)
    action = request.POST.get('action')  # delete_post | dismiss | warn

    if action == 'delete_post':
        report.post.is_deleted = True
        report.post.save()
        report.status      = 'resolved'
        report.reviewed_by = request.user
        report.resolved_at = timezone.now()
        report.save()
        Notification.objects.create(
            recipient=report.reporter,
            sender=request.user,
            notif_type='report',
            topic_id=report.post.topic.id,
            topic_title=report.post.topic.title,
        )
        messages.success(request, 'Đã xóa bài vi phạm.')

    elif action == 'dismiss':
        report.status      = 'dismissed'
        report.reviewed_by = request.user
        report.resolved_at = timezone.now()
        report.save()
        messages.info(request, 'Đã bỏ qua báo cáo.')

    elif action == 'warn':
        report.status      = 'resolved'
        report.reviewed_by = request.user
        report.resolved_at = timezone.now()
        report.save()
        Notification.objects.create(
            recipient=report.reporter,
            sender=request.user,
            notif_type='report',
            topic_id=report.post.topic.id,
            topic_title=report.post.topic.title,
        )
        messages.warning(request, f'Đã ghi nhận cảnh báo với {report.post.author.username}.')

    return redirect('moderation:dashboard')


@moderator_required
def toggle_lock_topic(request, topic_id):
    """Khóa / mở khóa chủ đề"""
    topic = get_object_or_404(Topic, id=topic_id)
    topic.is_locked = not topic.is_locked
    topic.save()
    status = 'khóa' if topic.is_locked else 'mở khóa'
    messages.success(request, f'Đã {status} chủ đề.')
    return redirect('topics:topic_detail', topic_id=topic.id)


@moderator_required
def ban_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, 'Không thể tự khóa tài khoản của mình.')
        return redirect('moderation:dashboard')
    if request.method == 'POST':
        target.is_active = not target.is_active
        target.save()
        action = 'mở khóa' if target.is_active else 'khóa'
        messages.success(request, f'Đã {action} tài khoản {target.username}.')
        return redirect('moderation:dashboard')
    return render(request, 'moderation/ban_confirm.html', {'target': target})


@moderator_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'moderation/user_list.html', {'users': users})


@moderator_required
def report_dashboard(request):
    today      = timezone.now().date()
    days       = int(request.GET.get('days', 7))
    start_date = today - timedelta(days=days - 1)

    posts_by_day = (
        Post.objects
        .filter(created_at__date__gte=start_date, is_deleted=False)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    members_by_day = (
        User.objects
        .filter(date_joined__date__gte=start_date)
        .annotate(date=TruncDate('date_joined'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    topics_by_forum = (
        Forum.objects
        .annotate(topic_count=Count('topics'))
        .values('forum_name', 'topic_count')
        .order_by('-topic_count')
    )

    active_users = (
        User.objects
        .annotate(post_count=Count('posts'))
        .order_by('-post_count')[:10]
    )

    context = {
        'posts_by_day':    list(posts_by_day),
        'members_by_day':  list(members_by_day),
        'topics_by_forum': list(topics_by_forum),
        'active_users':    active_users,
        'totals': [
            ('Tổng thành viên',    User.objects.count(),  '#3a86ff'),
            ('Tổng chủ đề',        Topic.objects.count(), '#e85d04'),
            ('Chuyên mục',         Forum.objects.count(), '#8338ec'),
            ('Thành viên hôm nay', User.objects.filter(date_joined__date=today).count(), '#06d6a0'),
        ],
        'days': days,
    }
    return render(request, 'moderation/report_dashboard.html', context)