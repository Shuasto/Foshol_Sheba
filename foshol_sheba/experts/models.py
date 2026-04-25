from django.db import models
from django.conf import settings

# Create your models here.

class ExpertProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'expert'},
        related_name='expert_profile'
    )
    specialization = models.CharField(max_length=255, help_text="e.g. Entomology, Plant Pathology")
    qualification = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    organization_association = models.CharField(max_length=255, blank=True, null=True, help_text="Current workplace or association")
    is_verified_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expert: {self.user.username} - {self.specialization}"

class ExpertAdvice(models.Model):
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='advices')
    diagnostic_record = models.ForeignKey('core.DiagnosticHistory', on_delete=models.CASCADE, related_name='expert_advices')
    advice_en = models.TextField(verbose_name="Professional Advice (English)")
    advice_bn = models.TextField(verbose_name="Professional Advice (Bangla)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advice from {self.expert.user.username} on {self.diagnostic_record.id}"
