from django import forms
from .models import UserInput

class UserInputForm(forms.ModelForm):
    class Meta:
        model = UserInput
        fields = ['university','school','name', 'st_year_mon','end_year_mon', 'note']
