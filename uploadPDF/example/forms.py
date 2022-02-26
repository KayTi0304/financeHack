from django import forms

class companyForm(forms.Form):
    company_name = forms.CharField(label="Company name", max_length=100)  