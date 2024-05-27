from unittest.util import _MAX_LENGTH
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import asset, student, teacher, User
from datetime import datetime
from django.core.validators import validate_comma_separated_integer_list
from django.forms.widgets import SelectDateWidget

class AssetForm(forms.ModelForm):

    class Meta:
        model = asset
        fields = ['Name', 'Location', 'Subject', 'Value', 'AssetImage'] #'__all__' for all

class AssetEventForm(forms.Form):
    LoanExpiry = forms.DateTimeField(widget=SelectDateWidget)
    Description = forms.CharField(max_length=100)
    UsersInvolved = forms.CharField(validators=[validate_comma_separated_integer_list])


class SignUpForm(UserCreationForm):
    # Extra fields added to user creation forms
    email = forms.EmailField(required=True)
    isTeacher = forms.BooleanField(label="Are you a Teacher?", required=False)
    teachingarea = forms.CharField(max_length = 30, label="If so, what area do you teach in?", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # overload
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        # if is a teacher, also add to teacher database
        if self.cleaned_data['isTeacher']:
            teacher.objects.create(user=user, Area = self.cleaned_data['teachingarea'])
        else:
            student.objects.create(user=user)
        return user # save must return user object
    

        """
        username = forms.CharField(label='username', max_length=50)
        email = forms.EmailField(label="email")
        password1 = forms.CharField(label='password', widget=forms.PasswordInput)
        password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

        # overload functions
        def username_clean(self):
            username = self.cleaned_data['username']
            if User.objects.filter(username=username).DoesNotExist:
                raise ValidationError("User Already Exists")
            return username
        
        def email_clean(self):
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).DoesNotExist:
                raise ValidationError("Email Already Exists")
            return email

        def clean_password2(self):
            username = self.cleaned_data['username']
            if User.objects.filter(username=username).DoesNotExist:
                raise ValidationError("User Already Exists")
            return username

        def save(self, commit=True):
            user = User.objects.create_user(self.cleaned_data['username'], 
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password1'])
            return user
        """

