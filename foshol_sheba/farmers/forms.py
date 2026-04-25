from django import forms
from core.models import User, Crop
from .models import FarmerProfile

class FarmerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'district', 'upazila', 'address', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার প্রথম নাম'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার শেষ নাম'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ইমেইল ঠিকানা'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'মোবাইল নম্বর'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'জেলা'}),
            'upazila': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'উপজেলা'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'বিস্তারিত ঠিকানা', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['farm_size_in_decimals', 'primary_crops']
        widgets = {
            'farm_size_in_decimals': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'খামারের আকার (শতাংশ)'}),
            'primary_crops': forms.SelectMultiple(attrs={'class': 'form-control d-none', 'id': 'crops-select'}),
        }
