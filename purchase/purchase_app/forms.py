from django import forms
from django.utils.translation import gettext_lazy as _
from .models import RequestModel


class RequestModelForm(forms.ModelForm):
    state = forms.ChoiceField(label=_('State'), choices=RequestModel.states.items(), widget=forms.Select(attrs={'class': 'form-control'}), initial=RequestModel.STATE_NEW)

    class Meta:
        model = RequestModel
        fields = ['registry_number', 'purchase_name', 'initial_price',
                  'bid_security_amount', 'work_security_amount',
                  'warranty_security_amount', 'warranty_period',
                  'bid_submission_deadline', 'contract_completion_date',
                  'comment', 'state']
        widgets = {
            'bid_submission_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'contract_completion_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].initial = RequestModel.STATE_NEW
