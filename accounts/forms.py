from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User


class RegisterForm(UserCreationForm):
    """Đăng ký — theo bảng 2.10: kiểm tra username, email, password"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email của bạn'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'display_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được đăng ký.')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Tên đăng nhập đã được sử dụng.')

        return username


class ProfileForm(forms.ModelForm):
    """Cập nhật hồ sơ cá nhân"""

    class Meta:
        model = User
        fields = ['display_name', 'avatar_url', 'bio', 'email']


# PasswordChangeForm từ Django dùng luôn