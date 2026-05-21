from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import User

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Chào mừng {user.display_name or user.username}!')
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})
@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    # Lấy bài viết gần đây của user này
    from topics.models import Topic
    recent_topics = Topic.objects.filter(
        author=profile_user
    ).order_by('-created_at')[:10]
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'recent_topics': recent_topics,
    })

@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None,
                       request.FILES or None,
                       instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cập nhật hồ sơ thành công.')
        return redirect('profile_view')
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)  # không bị đăng xuất
        messages.success(request, 'Đổi mật khẩu thành công.')
        return redirect('profile_view')
    return render(request, 'accounts/change_password.html', {'form': form})
@login_required
def manage_users(request):
    if request.user.role != 'admin':
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('home')

    users = User.objects.all().order_by('username')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        if user_id and new_role in ('user', 'moderator', 'admin'):
            target = get_object_or_404(User, id=user_id)
            if target == request.user:
                messages.error(request, 'Không thể tự đổi quyền của chính mình.')
            else:
                target.role = new_role
                target.is_staff = new_role in ('moderator', 'admin')
                target.is_superuser = new_role == 'admin'
                target.save()
                messages.success(request, f'Đã đổi quyền {target.username} thành {new_role}.')
        return redirect('accounts:manage_users')

    return render(request, 'accounts/manage_users.html', {'users': users})
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='123456789'
        )
        return HttpResponse("Admin created")

    return HttpResponse("Admin already exists")