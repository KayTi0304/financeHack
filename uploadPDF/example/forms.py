from tkinter.ttk import Style
from django import forms

class companyForm(forms.Form):
    company_name = forms.CharField(label="Company name", max_length=100, widget=forms.TextInput(attrs={
        'style': 'background: transparent; border: none; border-bottom: 2px solid lightgrey'
    }))  