from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'কৃষক'),
        ('expert', 'কৃষি বিশেষজ্ঞ'),
        ('company', 'কীটনাশক ও সার কোম্পানি'),
        ('admin', 'সিস্টেম অ্যাডমিনিস্ট্রেটর'),
    )
    
    phone_no = models.CharField(max_length=15, unique=True, db_index=True, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    upazila = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Crop(models.Model):
    name_en = models.CharField(max_length=100, verbose_name="Crop Name (English)")
    name_bn = models.CharField(max_length=100, verbose_name="Crop Name (Bangla)")
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_bn = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name_en} / {self.name_bn}"

class Disease(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='diseases')
    name_en = models.CharField(max_length=255, verbose_name="Disease Name (English)")
    name_bn = models.CharField(max_length=255, verbose_name="Disease Name (Bangla)")
    description_en = models.TextField()
    description_bn = models.TextField()
    symptoms_en = models.TextField()
    symptoms_bn = models.TextField()
    organic_remedy_en = models.TextField(verbose_name="Organic Remedy (English)")
    organic_remedy_bn = models.TextField(verbose_name="Organic Remedy (Bangla)")
    chemical_treatment_en = models.TextField(verbose_name="Chemical Treatment (English)")
    chemical_treatment_bn = models.TextField(verbose_name="Chemical Treatment (Bangla)")
    preventative_measures_en = models.TextField()
    preventative_measures_bn = models.TextField()
    is_expert_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name_en} ({self.crop.name_en})"

class DiagnosticHistory(models.Model):

    STATUS_CHOICES = (
        ('pending', 'অপেক্ষমান'),
        ('verified', 'যাচাইকৃত'),
        ('unverified', 'অযাচাইকৃত'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnostic_histories')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='diagnostic_histories', null=True, blank=True)
    crop_image = models.ImageField(upload_to='diagnostic_images/')
    detected_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_score = models.FloatField(blank=True, null=True)
    ai_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "DiagnosticHistories"
        ordering = ['-created_at']

    def __str__(self):
        disease_name = self.detected_disease.name_en if self.detected_disease else 'Unknown'
        crop_name = self.crop.name_en if self.crop else 'Unknown'
        return f"{self.user.username} - {crop_name}: {disease_name} ({self.created_at.date()})"

class MarketPrice(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    market_name = models.CharField(max_length=255)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop.name_en} - {self.market_name}: {self.price_per_kg} TK"

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='forum_images/', blank=True, null=True)
    related_diagnosis = models.ForeignKey(DiagnosticHistory, on_delete=models.SET_NULL, null=True, blank=True, related_name='forum_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Badge(models.Model):
    TYPE_CHOICES = (
        ('post', 'পোস্ট'),
        ('scan', 'স্ক্যান'),
        ('comment', 'মন্তব্য'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    required_count = models.IntegerField()
    icon = models.CharField(max_length=50, default="🏅")

    def __str__(self):
        return f"{self.title} ({self.get_badge_type_display()} - {self.required_count})"

class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
