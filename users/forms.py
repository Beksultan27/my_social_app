from django import forms
from django.contrib.auth.models import User

from .models import Profile

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

STATUS_CHOICES = [
    ('Married', 'Married'),
    ('Single', 'Single')
]

PROFESSION_CHOICES = [
    ('Student or Learning', 'Student or Learning'),
    ('Junior Developer', 'Junior Developer'),
    ('Senior Developer', 'Senior Developer'),
    ('Developer', 'Developer'),
    ('Manager', 'Manager'),
    ('Instructor or Teacher', 'Instructor or Teacher'),
    ('Intern', 'Intern'),
    ('ussiness Man', 'Bussiness Man'),
    ('Digital Marketer', 'Digital Marketer'),
    ('Data Scientist', 'Data Scientist'),
    ('Other', 'Other')
]

DEGREE_CHOICES = [
    ('IT', 'Information Technologies'),
    ('Bussiness Managment', 'Bussiness Managment'),
    ('Digital Marketing', 'Digital Marketing'),
    ('Computer Science', 'Computer Science'),
    ('Civil Engineering', 'Civil Engineering'),
    ('AI', 'Artificial & Inteligence'),
    ('Other', 'Other')
]


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Name'})
    )

    age = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Age'})
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg', })
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg', })
    )

    website = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Website'})
    )

    company = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Company'})
    )

    profession = forms.ChoiceField(
        choices=PROFESSION_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg'})
    )

    location = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Country'})
    )

    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Skills'})
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Country', 'rows': 4})
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control form-control-lg', })
    )

    class Meta:
        model = Profile
        fields = (
            'name', 'age', 'gender', 'status', 'website', 'company',
            'profession', 'location', 'skills', 'bio', 'image',)

    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data.get('age')
        if age > 50:
            raise forms.ValidationError('Age must be below 50 years!')
        elif age < 18:
            raise forms.ValidationError('Age must be at least 18 years!')
        else:
            return age
