from django import forms
from datetime import datetime
from django.contrib.auth.models import User
from .models import blogg, comment, profile
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm


class usersignupfrm(forms.Form):
    username = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Enter Username'})
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Enter your first name'})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Enter your last name'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Email is not valid'})
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required':'Enter Password'})
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required':'Re-Enter password'})

    def clean_username(self):
        uname = self.cleaned_data['username']
        if User.objects.filter(username=uname):
            raise forms.ValidationError('Username already taken.')
        return uname

    def clean_email(self):
        uemail = self.cleaned_data['email']
        if User.objects.filter(email=uemail):
            raise forms.ValidationError('Your email is already registered.')
        return uemail

    def clean_password2(self):
        upass = self.cleaned_data['password2']
        if len(upass)<8:
            raise forms.ValidationError('password must be more than 8 character.')
        return upass

class userloginfrm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Enter Username'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required':'Enter Password'})

    def clean_username(self):
        uname = self.cleaned_data['username']
        if User.objects.filter(username=uname):
            return uname
        else:
            raise forms.ValidationError('Invalid Username')


class modelblogggfrm(forms.ModelForm):
    class Meta():
        model = blogg
        fields = '__all__'
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'brief':forms.Textarea(attrs={'class':'form-control'}),
        'link':forms.TextInput(attrs={'class':'form-control'}),
        'date':forms.HiddenInput(),'dtn':forms.HiddenInput(),'user':forms.HiddenInput(),'name':forms.HiddenInput(),'likes':forms.HiddenInput()}
        labels = {'brief':'Description','link':'Any URL (optional)'}
        error_messages = {'title':{'required':'title is empty.'},'brief':{'required':'you need to write your title description.'}}

class passwordfrm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required':'Enter old password'})
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='New password',error_messages={'required':'Enter new password'})
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Confirm password',error_messages={'required':'Confirm new password'})

class userchangefrm(UserChangeForm):
    password = None
    class Meta():
        model = User
        fields = ['username','first_name','last_name','email','date_joined','last_login']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),'email':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
        'date_joined':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),'last_login':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),}

class adminchangefrm(UserChangeForm):
    password = None
    class Meta():
        model = User
        fields = '__all__'
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),'email':forms.TextInput(attrs={'class':'form-control'}),
        'date_joined':forms.TextInput(attrs={'class':'form-control'}),'last_login':forms.TextInput(attrs={'class':'form-control'})}


class commentform(forms.ModelForm):
    class Meta():
        model = comment
        fields = ['content']
        labels = {'content':'Comment'}
        widgets = {'content':forms.TextInput(attrs={'class':'form-control'})}

class datecustom(forms.DateInput):
    input_type = 'date'

class profileform(forms.ModelForm):
    class Meta():
        model = profile
        fields = ['profile_id','dob','dp']
        labels = {'dob':'Date of Birth','dp':'Profile picture'}
        widgets = {'profile_id':forms.HiddenInput(),'dob':datecustom(attrs={'class':'form-control'})}