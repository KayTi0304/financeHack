from django import forms

class uploadFileForms(forms.Form):
    file = forms.FileField()    