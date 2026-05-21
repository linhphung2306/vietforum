from django import forms
from .models import Topic, Post

class TopicForm(forms.ModelForm):
    """Bảng 2.11: title 10-255 ký tự, content tối thiểu 20 ký tự"""
    class Meta:
        model  = Topic
        fields = ['title', 'content']
        widgets = {
            'title':   forms.TextInput(attrs={'placeholder': 'Tiêu đề (10–255 ký tự)'}),
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Nội dung...'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 10:
            raise forms.ValidationError('Tiêu đề phải có ít nhất 10 ký tự.')
        return title
    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) < 20:
            raise forms.ValidationError('Nội dung phải có ít nhất 20 ký tự.')
        return content

class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['content', 'parent_post']
        widgets = {
            'content':     forms.Textarea(attrs={'rows': 5}),
            'parent_post': forms.HiddenInput(),
        }