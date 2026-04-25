from django.db import models
from django.conf import settings

# Create your models here.

class FarmerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'farmer'},
        related_name='farmer_profile'
    )
    primary_crops = models.ManyToManyField('core.Crop', related_name='farmers', blank=True)
    farm_size_in_decimals = models.FloatField(blank=True, null=True, help_text="Size of the farm in decimals")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Farmer: {self.user.username}"
