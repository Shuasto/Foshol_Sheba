from django import forms
from core.models import User
from .models import ExpertProfile

class ExpertUserForm(forms.ModelForm):
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

class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['specialization', 'qualification', 'experience_years', 'organization_association']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বিশেষত্ব (যেমন: এন্টোমোলজি, প্লান্ট প্যাথলজি)'}),
            'qualification': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'যোগ্যতা (শিক্ষাগত এবং অন্যান্য)', 'rows': 3}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'অভিজ্ঞতা (বছর)'}),
            'organization_association': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বর্তমান কর্মস্থল বা সমিতি'}),
        }
