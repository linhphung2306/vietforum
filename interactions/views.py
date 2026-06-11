from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from topics.models import Post
from .models import Vote, Report
from .forms import ReportForm


@login_required
@require_POST
def vote(request, post_id):
    post      = get_object_or_404(Post, id=post_id, is_deleted=False)
    vote_type = request.POST.get('vote_type')

    if vote_type not in ('like', 'dislike'):
        return JsonResponse({'error': 'invalid'}, status=400)

    existing = Vote.objects.filter(post=post, user=request.user).first()

    if existing:
        if existing.vote_type == vote_type:
            existing.delete()
        else:
            existing.vote_type = vote_type
            existing.save()
    else:
        Vote.objects.create(post=post, user=request.user, vote_type=vote_type)

    likes    = post.votes.filter(vote_type='like').count()
    dislikes = post.votes.filter(vote_type='dislike').count()
    return JsonResponse({'likes': likes, 'dislikes': dislikes})


@login_required
def report(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_deleted=False)

    if post.author == request.user:
        messages.error(request, 'Không thể báo cáo bài viết của chính mình.')
        return redirect('topics:topic_detail', topic_id=post.topic.id)

    if Report.objects.filter(post=post, reporter=request.user).exists():
        messages.warning(request, 'Bạn đã báo cáo bài viết này rồi.')
        return redirect('topics:topic_detail', topic_id=post.topic.id)

    form = ReportForm(request.POST or None)
    if form.is_valid():
        r          = form.save(commit=False)
        r.post     = post
        r.reporter = request.user
        r.save()
        messages.success(request, 'Đã gửi báo cáo. Cảm ơn bạn!')
        return redirect('topics:topic_detail', topic_id=post.topic.id)

    return render(request, 'interactions/report_form.html', {
        'form': form,
        'post': post,
    })