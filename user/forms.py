# Import necessary modules from Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from .models import CustomUser

# SignupForm class to handle user registration
class SignupForm(UserCreationForm):
    # Phone number field to capture user's phone number
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your phone number.",
        error_messages={
            'required': 'Please provide your phone number.',
            'max_length': 'Phone number cannot exceed 15 characters.',
        }
    )
    
    # Address field to capture user's address
    address = forms.CharField(
        required=True,
        help_text="Enter your address.",
        error_messages={
            'required': 'Please provide your address.',
        }
    )
    
    # Company name field, optional for property owners
    company_name = forms.CharField(
        max_length=255,
        required=False,
        help_text="If you're a property owner, enter your company name.",
    )
    
    # Date of birth field with a date picker widget
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Enter your date of birth.",
        error_messages={
            'required': 'Please provide your date of birth.',
        }
    )
    
    # User type field with predefined choices for user role
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        required=True,
        help_text="Select your user type.",
        error_messages={
            'required': 'Please select your user type.',
        }
    )

    class Meta:
        # Specify the model and fields for the form
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

    # Custom validation for phone number field
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Check if the phone number contains only digits and '+' for international format
        if not phone_number.replace("+", "").isdigit():
            raise forms.ValidationError("Phone number must contain only digits and '+' for international format.")
        # Check if the phone number has at least 10 digits
        if len(phone_number) < 10:
            raise forms.ValidationError("Phone number must have at least 10 digits.")
        return phone_number

    # Custom validation for the date of birth field to ensure the user is at least 18
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old to register.")
        return dob


# LoginForm class to handle user login
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)  # Email field for login
    password = forms.CharField(widget=forms.PasswordInput)  # Password field with a hidden input


# EmailAuthenticationForm class for authenticating users via email and password
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()  # Email field for authentication
    password = forms.CharField(widget=forms.PasswordInput)  # Password field with a hidden input

    # Custom validation for checking if the email and password are correct
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            # Authenticate the user using Django's built-in authentication system
            self.user = authenticate(email=email, password=password)
            if not self.user:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data

    # Method to return the authenticated user
    def get_user(self):
        return self.user


# PasswordResetRequestForm to request a password reset
class PasswordResetRequestForm(forms.Form):
    # Email field for the user to enter their email address for password reset
    email = forms.EmailField(label="Enter your email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
