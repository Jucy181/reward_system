from django import forms
from core.models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name','description','image','points','status']