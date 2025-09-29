from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['app', 'screenshot']
        widgets = {
            'app': forms.Select(attrs={'class': 'form-control'}),
            'screenshot': forms.FileInput(attrs={'class': 'form-control'}),

        }
