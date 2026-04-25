from django.contrib import admin
from .models import ExpertProfile, ExpertAdvice

@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_verified_by_admin', 'created_at')
    list_filter = ('is_verified_by_admin', 'specialization', 'created_at')
    search_fields = ('user__username', 'specialization', 'qualification')
    actions = ['verify_experts']

    def verify_experts(self, request, queryset):
        queryset.update(is_verified_by_admin=True)
    verify_experts.short_description = "Mark selected experts as verified"

@admin.register(ExpertAdvice)
class ExpertAdviceAdmin(admin.ModelAdmin):
    list_display = ('expert', 'diagnostic_record', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('advice_en', 'expert__user__username')
    readonly_fields = ('created_at',)
