from django import forms
from django.utils.translation import gettext_lazy as _
from .models import RequestModel, StateRequestModel


class RequestModelForm(forms.ModelForm):

    class Meta:
        model = RequestModel
        fields = ['registry_number', 'purchase_name', 'initial_price',
                  'bid_security_amount', 'work_security_amount',
                  'warranty_security_amount', 'warranty_period',
                  'bid_submission_deadline', 'contract_completion_date',
                  'comment',]
        widgets = {
            'bid_submission_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'contract_completion_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class StateRequestModelForm(forms.ModelForm):
    name = forms.ChoiceField(choices=StateRequestModel.STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    order = forms.IntegerField(required=False)
    description = forms.CharField(max_length=255, required=False)

    class Meta:
        model = StateRequestModel
        fields = ['name', 'order', 'description']
