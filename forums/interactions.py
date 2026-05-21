from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model  = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Mô tả lý do báo cáo...',
            })
        }
        labels = {'reason': 'Lý do báo cáo'}