from django import forms
from .models import Post


class SearchForm(forms.Form):
    query = forms.CharField()


class PostModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Title'})
    )

    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Description', 'rows': 3})
    )

    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ('title', 'description', 'image')

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if not title.strip():
            raise forms.ValidationError('Invalid title!')
        else:
            return title

    def clean_description(self, *args, **kwargs):
        description = self.cleaned_data.get('description')
        if not description.strip():
            raise forms.ValidationError('Invalid description!')
        else:
            return description



