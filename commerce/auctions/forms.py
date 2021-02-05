from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from .models import User, UserProfile, Listing, Bid

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
    
    class Meta:
        model = Listing
        fields = ('title','min_bid','description')
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control'}),
            'description':forms.Textarea(attrs={
                'class':'form-control'}),
            'min_bid':forms.NumberInput(attrs={
                'class':'form-control'})
        }

class CreateBidForm(forms.ModelForm):
    listing = forms.ModelChoiceField(label="", queryset=Listing.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = Bid
        fields = ['amount','bidder','listing',]
        widgets = {
            'amount':forms.NumberInput(attrs={
                'class':'form-control'}),
            'bidder':forms.HiddenInput(),
            'listing':forms.HiddenInput()
            
        }
        
    # clean method ensures the bid amount is greater than the highest bid or min_bid of listing
    def clean(self):
        cleaned_data = super(CreateBidForm,self).clean()
        amount = cleaned_data.get("amount")
        self.fields.get('amount').validate(amount)
        listing = cleaned_data.get("listing")
        bids = listing.bids.all()
        if len(bids) != 0:
            highest_bid = bids.aggregate(Max('amount'))
            if highest_bid <= amount:
                raise ValidationError(f"Must bid higher than the highest bid which is ${highest_bid.amount}.")
        elif listing.min_bid > amount:
            raise ValidationError(f"Must bid higher than the listing's minimum bid, ${listing.min_bid}.")
                
