from django import forms
from .models import Resource
from apps.subjects.models import Topic


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['topic', 'title', 'resource_type', 'file', 'url', 'text_content']
        widgets = {
            'topic': forms.Select(attrs={'class': 'cyber-input'}),
            'title': forms.TextInput(attrs={
                'class': 'cyber-input',
                'placeholder': 'Resurs sarlavhasi'
            }),
            'resource_type': forms.Select(attrs={
                'class': 'cyber-input',
                'id': 'resource_type_select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'cyber-file-input',
                'accept': '.pdf'
            }),
            'url': forms.URLInput(attrs={
                'class': 'cyber-input',
                'placeholder': 'https://...'
            }),
            'text_content': forms.Textarea(attrs={
                'class': 'cyber-input',
                'placeholder': 'Matnni shu yerga kiriting...',
                'rows': 6
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        resource_type = cleaned_data.get('resource_type')
        file = cleaned_data.get('file')
        url = cleaned_data.get('url')
        text_content = cleaned_data.get('text_content')

        if resource_type == 'pdf' and not file:
            raise forms.ValidationError("PDF turida fayl yuklash majburiy.")
        if resource_type == 'url' and not url:
            raise forms.ValidationError("URL turida havola kiritish majburiy.")
        if resource_type == 'text' and not text_content:
            raise forms.ValidationError("Matn turida matn kiritish majburiy.")
        return cleaned_data
