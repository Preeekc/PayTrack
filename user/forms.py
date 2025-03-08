from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from .models import CustomUser

class SignupForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your phone number.",
        error_messages={
            'required': 'Please provide your phone number.',
            'max_length': 'Phone number cannot exceed 15 characters.',
        }
    )
    address = forms.CharField(
        required=True,
        help_text="Enter your address.",
        error_messages={
            'required': 'Please provide your address.',
        }
    )
    company_name = forms.CharField(
        max_length=255,
        required=False,
        help_text="If you're a property owner, enter your company name.",
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Enter your date of birth.",
        error_messages={
            'required': 'Please provide your date of birth.',
        }
    )
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        required=True,
        help_text="Select your user type.",
        error_messages={
            'required': 'Please select your user type.',
        }
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'phone_number',
            'address',
            'company_name',
            'date_of_birth',
            'user_type'
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.replace("+", "").isdigit():
            raise forms.ValidationError("Phone number must contain only digits and '+' for international format.")
        if len(phone_number) < 10:
            raise forms.ValidationError("Phone number must have at least 10 digits.")
        return phone_number

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old to register.")
        return dob



from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from django.contrib.auth import authenticate

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if not self.user:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data

    def get_user(self):
        return self.user


# forms.py
from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
