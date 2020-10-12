# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import province, county, blood_group, UserProfile, blood_share, feedback, Message, HomeRightInformation


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False,max_length=30)
    last_name = forms.CharField(required=False,max_length=50)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email zaten mevcut")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','blood_group','province','county','birth_date', 'privacy')

    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['county'].queryset = county.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['county'].queryset = county.objects.filter(province_id=province_id).order_by('county_name')
            except (ValueError, TypeError):
                pass # invalid input from the user; ignore and fallback to empty County queryset

class UserRegistrationUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=50)

    class Meta:
        model = User
        fields = ('username','first_name','last_name')

class UserProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(required=True,max_length=30)
    class Meta:
        model = UserProfile
        fields = ('phone','blood_group','province','county','birth_date', 'privacy')

class provinceForm(forms.ModelForm):
    class Meta:
        model = province
        fields = ("province_id","province_name")

class countyForm(forms.ModelForm):
    class Meta:
        model = county
        fields = ("county_id","county_name","province_id")

class blood_groupForm(forms.ModelForm):
    class Meta:
        model = blood_group
        fields = ("blood_id","blood_name")

class feedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ("name","message")

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("message",)

class HomeRightInformationForm(forms.ModelForm):
    class Meta:
        model = HomeRightInformation
        fields = ("content","written_by")

BLOOD_CHOICES = (
   ('kan arıyor', 'Kan arıyorum'),
   ('kan veriyor', 'Kan veriyorum')
)

class blood_shareForm(forms.ModelForm):
    choice = forms.ChoiceField(choices=BLOOD_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = blood_share
        fields = ("blood_group","province","county","date_range","searching_reason","contact_name","contact_number","choice")

    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['county'].queryset = county.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['county'].queryset = county.objects.filter(province_id=province_id).order_by('county_name')
            except (ValueError, TypeError):
                pass # invalid input from the user; ignore and fallback to empty County queryset


class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )
