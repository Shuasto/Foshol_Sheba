from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('herbicide', 'Herbicide'),
        ('fungicide', 'Fungicide'),
        ('other', 'Other'),
    )

    company = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'company'},
        related_name='products'
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    crops = models.ManyToManyField('core.Crop', related_name='products', blank=True)
    target_diseases = models.ManyToManyField('core.Disease', related_name='recommended_products', blank=True)
    description = models.TextField()
    usage_guidelines = models.TextField()
    price_info = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.company.username}"
