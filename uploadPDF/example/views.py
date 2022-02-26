from django.shortcuts import redirect, render
from django.http import HttpResponse
from urllib.parse import urlencode
from django.urls import reverse
from .forms import companyForm

# Create your views here.
def welcome(request):
    if request.method == 'POST':
        return HttpResponse("You probably shouldn't be seeing this")
    else:
        form = companyForm()
        return render(request, 'administration/upload.html', {'form': form})

def display_report(request):
    if request.method == 'POST':
        form = companyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['company_name']
            return render(request, 'administration/display.html', {'name': name})
    else:
        form = companyForm()
        return render(request, 'administration/upload.html', {'form': form})