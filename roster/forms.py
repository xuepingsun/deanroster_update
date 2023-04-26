from django import forms
from .models import DeanBasic, SchoolInfo#UserInput,

# class UserInputForm(forms.ModelForm):
#     class Meta:
#         model = UserInput
#         fields = ['university','school','name', 'st_year_mon','end_year_mon', 'note']

class DeanBasicForm(forms.ModelForm):
    category=forms.ModelChoiceField(
        queryset=SchoolInfo.objects.all(),
        widget=forms.Select()
    )
    class Meta:
        model = DeanBasic
        fields = "__all__" #'university','school','name', 'st_year_mon','end_year_mon', 'CV_string']
        #"__all__" #[
