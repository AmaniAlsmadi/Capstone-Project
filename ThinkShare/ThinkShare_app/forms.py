from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Article,Comment,Contact

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address")
    username = forms.CharField(max_length=30, required=True, help_text="Required")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required")
    
    class Meta:
        model = User
        fields = [ 'email','username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This user name is already taken.")
        return username
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'link', 'category']
        widgets = {
    'content': forms.Textarea(attrs={'rows': 8, 'id': 'content'}),
}

class CommentForm(forms.ModelForm):
   class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields = ['name', 'email', 'message']
