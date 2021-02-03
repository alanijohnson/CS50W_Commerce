from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, UserProfile, Listing

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'})
        }
        labels = {
            'first_name':'',
            'last_name':''
        }

class CreateListingForm(forms.ModelForm):
    model = Listing
    fields = ('title','description')
    widgets = {
        'title':forms.TextInput(attrs={
            'class':'form-control'}),
        'description':forms.Textarea(attrs={
            'class':'form-control'})
    }
