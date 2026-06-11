from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q, Count
import re
from forums.models import Forum
from .models import Topic, Post, Attachment
from .forms import TopicForm, PostForm


def forum_detail(request, forum_id):
    forum  = get_object_or_404(Forum, id=forum_id, is_active=True)
    topics = forum.topics.all()
    page   = Paginator(topics, 20).get_page(request.GET.get('page'))
    return render(request, 'topics/forum_detail.html', {
        'forum': forum, 'page': page,
    })


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'GET':
        Topic.objects.filter(id=topic_id).update(
            view_count=models.F('view_count') + 1
        )
        topic.refresh_from_db()

    posts = topic.posts.filter(is_deleted=False).annotate(
        like_count=Count('votes', filter=Q(votes__vote_type='like')),
        dislike_count=Count('votes', filter=Q(votes__vote_type='dislike'))
    )
    page  = Paginator(posts, 20).get_page(request.GET.get('page'))
    form  = PostForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if topic.is_locked:
            messages.error(request, 'Chủ đề này đã bị khóa, không thể phản hồi.')
            return redirect('topics:topic_detail', topic_id=topic.id)
        form = PostForm(request.POST)
        if form.is_valid():
            post            = form.save(commit=False)
            post.topic      = topic
            post.author     = request.user
            parent_id       = request.POST.get('parent_post')
            if parent_id:
                post.parent_post = Post.objects.filter(
                    id=parent_id, is_deleted=False
                ).first()
            post.save()

            # Xử lý upload file/ảnh đính kèm cho post
            for f in request.FILES.getlist('attachments'):
                file_type = 'image' if f.content_type.startswith('image/') else 'file'
                Attachment.objects.create(
                    post=post,
                    author=request.user,
                    file=f,
                    file_name=f.name,
                    file_type=file_type,
                )

            return redirect('topics:topic_detail', topic_id=topic.id)

    return render(request, 'topics/topic_detail.html', {
        'topic': topic, 'page': page, 'form': form,
    })


@login_required
def create_topic(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id, is_active=True)
    if not request.user.is_active:
        messages.error(request, 'Tài khoản của bạn đã bị khóa.')
        return redirect('home')
    form = TopicForm(request.POST or None)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.forum  = forum
        topic.author = request.user
        topic.save()

        # Xử lý upload file/ảnh đính kèm cho topic
        for f in request.FILES.getlist('attachments'):
            file_type = 'image' if f.content_type.startswith('image/') else 'file'
            Attachment.objects.create(
                topic=topic,
                author=request.user,
                file=f,
                file_name=f.name,
                file_type=file_type,
            )

        messages.success(request, 'Tạo chủ đề thành công!')
        return redirect('topics:topic_detail', topic_id=topic.id)
    return render(request, 'topics/create_topic.html', {
        'form': form, 'forum': forum,
    })


@login_required
def edit_topic(request, topic_id):
    from django.core.exceptions import PermissionDenied
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user and not request.user.is_mod_or_admin():
        raise PermissionDenied
    form = TopicForm(request.POST or None, instance=topic)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cập nhật chủ đề thành công.')
        return redirect('topics:topic_detail', topic_id=topic.id)
    return render(request, 'topics/edit_topic.html', {
        'form': form, 'topic': topic,
    })


@login_required
def delete_post(request, post_id):
    from django.core.exceptions import PermissionDenied
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_mod_or_admin():
        raise PermissionDenied
    post.is_deleted = True
    post.save()
    return redirect('topics:topic_detail', topic_id=post.topic.id)


def search(request):
    keyword   = request.GET.get('q', '').strip()
    forum_id  = request.GET.get('forum', '')
    author_kw = request.GET.get('author', '').strip()
    sort_by   = request.GET.get('sort', 'newest')

    keyword_clean = re.sub(r'[^\w\s]', '', keyword)
    author_clean  = re.sub(r'[^\w\s]', '', author_kw)

    results = Topic.objects.filter(forum__is_active=True)

    if keyword_clean:
        results = results.filter(
            Q(title__icontains=keyword_clean) |
            Q(content__icontains=keyword_clean)
        )

    if forum_id:
        results = results.filter(forum_id=forum_id)

    if author_clean:
        results = results.filter(
            Q(author__username__icontains=author_clean) |
            Q(author__display_name__icontains=author_clean)
        )

    sort_map = {
        'newest':  '-created_at',
        'oldest':  'created_at',
        'popular': '-view_count',
    }
    results = results.order_by(sort_map.get(sort_by, '-created_at'))

    paginator  = Paginator(results, 20)
    page_obj   = paginator.get_page(request.GET.get('page'))
    forums_all = Forum.objects.filter(is_active=True)

    return render(request, 'topics/search.html', {
        'results':   page_obj,
        'query':     keyword,
        'author':    author_kw,
        'forums':    forums_all,
        'sort':      sort_by,
        'forum_id':  forum_id,
        'total':     paginator.count,
    })


@login_required
def pin_topic(request, topic_id):
    from django.core.exceptions import PermissionDenied
    topic = get_object_or_404(Topic, id=topic_id)
    if not request.user.is_mod_or_admin():
        raise PermissionDenied
    topic.is_pinned = not topic.is_pinned
    topic.save()
    messages.success(request, 'Đã ghim chủ đề.' if topic.is_pinned else 'Đã bỏ ghim.')
    return redirect('topics:forum_detail', forum_id=topic.forum.id)


@login_required
def edit_post(request, post_id):
    from django.core.exceptions import PermissionDenied
    post = get_object_or_404(Post, id=post_id, is_deleted=False)
    if post.author != request.user and not request.user.is_mod_or_admin():
        raise PermissionDenied
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Đã cập nhật bài viết.')
        return redirect('topics:topic_detail', topic_id=post.topic.id)
    return render(request, 'topics/edit_post.html', {
        'form': form, 'post': post,
    })