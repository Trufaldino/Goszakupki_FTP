from django import forms
from .models import RequestModel

class RequestModelForm(forms.ModelForm):
    class Meta:
        model = RequestModel
        fields = ['title', 'description', 'status', 'auction_date', 'price', 'completion_date', 'comment']
        widgets = {
            'auction_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }
