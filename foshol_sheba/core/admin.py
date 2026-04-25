from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, Crop, Disease, DiagnosticHistory, MarketPrice, CommunityPost, Comment, Badge

# Core Administrative Dashboard setup

class DiseaseInline(admin.TabularInline):
    model = Disease
    extra = 1

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_no', 'profile_picture', 'district', 'upazila', 'address')}),
    )
    list_display = ('username', 'email', 'role', 'phone_no', 'district', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone_no', 'district')

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn')
    search_fields = ('name_en', 'name_bn')
    inlines = [DiseaseInline]

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'crop', 'is_expert_verified')
    list_filter = ('crop', 'is_expert_verified')
    search_fields = ('name_en', 'name_bn', 'description_en', 'symptoms_en')

@admin.register(DiagnosticHistory)
class DiagnosticHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'detected_disease', 'confidence_score', 'created_at')
    list_filter = ('detected_disease', 'created_at')
    search_fields = ('user__username', 'detected_disease__name_en')
    readonly_fields = ('created_at',)

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop', 'market_name', 'price_per_kg', 'updated_at')
    list_filter = ('crop', 'updated_at')
    search_fields = ('market_name', 'crop__name_en')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'user__username')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'post__title')
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_type', 'required_count', 'icon')
    list_filter = ('badge_type',)
    search_fields = ('title', 'description')
