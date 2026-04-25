from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import DiagnosticHistory, CommunityPost, Crop, Disease, MarketPrice
from core.services.badge_service import get_user_badges
from core.services.pdf_export_service import generate_diagnosis_pdf
from farmers.forms import FarmerUserForm, FarmerProfileForm
from farmers.services.ai_checker import AICheckerService
import threading
from django.db import connection
import os
import datetime
from django.conf import settings

def run_ai_check_in_background(diagnosis_id):
    log_file_path = os.path.join(settings.BASE_DIR, 'ai_check_logs.txt')
    
    def write_log(message):
        try:
            with open(log_file_path, 'a', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] Diagnosis ID {diagnosis_id}: {message}\n")
        except Exception:
            pass
            
    write_log("Starting AI check process")
    
    try:
        diagnosis = DiagnosticHistory.objects.get(pk=diagnosis_id)
        write_log(f"Fetched DiagnosisHistory. Image path: {diagnosis.crop_image.path}")
        
        ai_service = AICheckerService()
        result = ai_service.analyze_image(diagnosis.crop_image.path)
        write_log(f"AI Service Result: {result}")
        
        if result.get('status') == 'success':
            data = result.get('data', {})
            disease_name = data.get('disease')
            confidence = data.get('confidence_score', 0.0)
            description = data.get('description', '')
            
            write_log(f"Success. Parsed data - Disease: {disease_name}, Confidence: {confidence}")
            
            if disease_name:
                try:
                    # Try finding the disease case-insensitively
                    disease = Disease.objects.get(name_en__iexact=disease_name)
                    diagnosis.detected_disease = disease
                    diagnosis.status = 'verified'
                    write_log("Disease mapped to DB model successfully")
                except Disease.DoesNotExist:
                    write_log("Disease not found in DB")
                    diagnosis.status = 'unverified'
            else:
                diagnosis.status = 'unverified'
                    
            diagnosis.confidence_score = float(confidence)
            diagnosis.ai_description = description
        else:
            diagnosis.status = 'unverified'
            
        diagnosis.save()
        write_log("Successfully updated and saved diagnosis history")
    except Exception as e:
        write_log(f"Error encountered: {str(e)}")
        try:
            diagnosis = DiagnosticHistory.objects.get(pk=diagnosis_id)
            diagnosis.status = 'unverified'
            diagnosis.save()
            write_log("Status set to unverified due to error")
        except Exception as inner_e:
            write_log(f"Error while setting unverified status: {str(inner_e)}")
            pass
    finally:
        connection.close()
        write_log("Database connection closed. Process finished.\n")

# Create your views here.

@login_required
def farmer_dashboard(request):
    from farmers.models import FarmerProfile
    from core.models import CommunityPost
    from itertools import chain
    
    profile, created = FarmerProfile.objects.get_or_create(user=request.user)
    is_profile_incomplete = (profile.primary_crops.count() == 0 or profile.farm_size_in_decimals is None)
    
    # Fetch diagnostic histories
    histories = DiagnosticHistory.objects.filter(user=request.user)
    # Fetch user's community posts
    posts = CommunityPost.objects.filter(user=request.user)
    
    # Combine and sort by created_at descending
    activities = sorted(
        chain(histories, posts),
        key=lambda x: x.created_at,
        reverse=True
    )[:10]
    
    total_diagnoses = histories.count()
    market_prices = MarketPrice.objects.all().order_by('-updated_at')[:4]
    recent_prices_count = MarketPrice.objects.all().count()
    
    return render(request, 'dashboards/farmer.html', {
        'activities': activities,
        'total_diagnoses': total_diagnoses,
        'recent_prices_count': recent_prices_count,
        'prices': market_prices,
        'user': request.user,
        'is_profile_incomplete': is_profile_incomplete
    })

@login_required
def diagnose_crop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        image_data = request.FILES.get('crop_image')
        
        if crop_id and image_data:
            crop = Crop.objects.get(id=crop_id)
            diagnosis = DiagnosticHistory.objects.create(
                user=request.user,
                crop=crop,
                crop_image=image_data,
                confidence_score=0.0,
                status='pending'
            )
            
            # Start background thread for AI analysis
            thread = threading.Thread(target=run_ai_check_in_background, args=(diagnosis.pk,))
            thread.daemon = True
            thread.start()
            
            messages.success(request, "আপনার ফসলের ছবি সফলভাবে আপলোড করা হয়েছে। কৃত্রিম বুদ্ধিমত্তা এটি বিশ্লেষণ করছে...")
            return redirect('farmers:diagnostic_result', pk=diagnosis.pk)
        else:
            messages.error(request, "অনুগ্রহ করে একটি ফসল এবং ছবি প্রদান করুন।")
            
    crops = Crop.objects.all()
    return render(request, 'farmers/farmer_create_diagnosis.html', {
        'crops': crops
    })

@login_required
def diagnostic_result(request, pk):
    result = DiagnosticHistory.objects.get(pk=pk)
    # Check if this diagnosis has already been shared in the forum
    existing_post = result.forum_posts.first()
    return render(request, 'core/result.html', {
        'result': result,
        'existing_post': existing_post
    })

@login_required
def diagnostic_history(request):
    histories = DiagnosticHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/history.html', {'histories': histories})

@login_required
def profile_view(request):
    from farmers.models import FarmerProfile
    profile, created = FarmerProfile.objects.get_or_create(user=request.user)
    earned_badges = get_user_badges(request.user)
    return render(request, 'profile/farmer_profile.html', {
        'profile': profile,
        'user': request.user,
        'badges': earned_badges
    })

@login_required
def edit_profile(request):
    from  farmers.models import FarmerProfile
    profile, created = FarmerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = FarmerUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = FarmerProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "আপনার প্রোফাইল সফলভাবে আপডেট করা হয়েছে।")
            return redirect('farmers:profile')
    else:
        user_form = FarmerUserForm(instance=request.user)
        profile_form = FarmerProfileForm(instance=profile)
        
    all_crops = Crop.objects.all()
    
    return render(request, 'profile/farmer_edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'all_crops': all_crops,
        'selected_crops': profile.primary_crops.all()
    })

@login_required
def export_diagnosis_pdf(request, pk):
    result = get_object_or_404(DiagnosticHistory, pk=pk, user=request.user)
    return render(request, 'core/diagnosis_pdf_template.html', {'result': result})