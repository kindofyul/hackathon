from django import forms
from .models import AltTextInfo

class AltTextForm(forms.ModelForm):
    class Meta:
        model = AltTextInfo
        fields = ['excel_file']