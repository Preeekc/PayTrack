from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('tenant', 'Tenant'),
        ('home owner', 'Home Owner'),
    )

    email = models.EmailField(unique=True,null=True)  # Ensuring unique emails for authentication
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Login with email instead of username
    REQUIRED_FIELDS = ['username']  # Keep username as an optional field if necessary

    def __str__(self):
        return self.email  # Display email instead of username


from django.db import models
from django.conf import settings

class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land'),
    ]
    # In your Property model
    homeowner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        null=True,  # Make it nullable temporarily
        blank=True  # Allow it to be blank temporarily
    )
    
    # In your Property model

    title = models.CharField(max_length=200, default="Unnamed Property")
    location = models.CharField(max_length=200, default="Unknown Location")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='house')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bedrooms = models.IntegerField(null=True, blank=True, default=1)
    bathrooms = models.IntegerField(null=True, blank=True, default=1)
    description = models.TextField(default="No description available.")
    image = models.ImageField(upload_to='properties/', default='default_property.jpg')
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title