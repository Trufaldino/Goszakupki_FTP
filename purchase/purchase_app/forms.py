from django import forms
from .models import RequestModel


class RequestModelForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=RequestModel.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус',
    )

    class Meta:
        model = RequestModel
        fields = ['registry_number', 'purchase_name', 'initial_price',
                  'bid_security_amount', 'work_security_amount',
                  'warranty_security_amount', 'warranty_period',
                  'bid_submission_deadline', 'contract_completion_date',
                  'comment', 'status',]
        widgets = {
            'bid_submission_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'contract_completion_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
