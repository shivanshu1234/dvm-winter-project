from django import forms
from .models import Post, Comment, Report
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewPostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('heading', 'text')

class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('heading', 'text')

class UserCreationFormWithEmail(UserCreationForm):
    
    email = forms.EmailField(required = True)

    class Meta:

        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit = True):
        user = super(UserCreationFormWithEmail, self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id = self.instance.id).filter(username = username).exists():
            raise forms.ValidationError("Username is already in use.")
        return username
        
class NewReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ("reason", "detailed_reason")
        

    
