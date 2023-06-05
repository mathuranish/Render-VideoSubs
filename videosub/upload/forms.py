from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

    
class SearchWordForm(forms.Form):
    keyword = forms.CharField(max_length=100)