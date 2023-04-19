from django import forms
from .models import DeanInfo #UserInput,

# class UserInputForm(forms.ModelForm):
#     class Meta:
#         model = UserInput
#         fields = ['university','school','name', 'st_year_mon','end_year_mon', 'note']

class DeanInfoForm(forms.ModelForm):
    class Meta:
        model = DeanInfo
        fields = "__all__" #'university','school','name', 'st_year_mon','end_year_mon', 'CV_string']
        #"__all__" #[
