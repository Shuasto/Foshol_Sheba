from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import DiagnosticHistory
from experts.models import ExpertProfile, ExpertAdvice
from experts.forms import ExpertUserForm, ExpertProfileForm

@login_required
def review_diagnosis(request, pk):
    if request.user.role != 'expert':
        return redirect('core:index')
    
    expert_profile, _ = ExpertProfile.objects.get_or_create(user=request.user)
    
    if not expert_profile.is_verified_by_admin:
        messages.error(request, "আপনার অ্যাকাউন্টটি এখনও ভেরিফাই করা হয়নি।")
        return redirect('core:expert_dashboard')

    record = get_object_or_404(DiagnosticHistory, pk=pk)
    
    if ExpertAdvice.objects.filter(diagnostic_record=record).exists():
        messages.info(request, "এই স্ক্যানটির জন্য ইতিমধ্যে একজন বিশেষজ্ঞের পরামর্শ দেওয়া হয়েছে।")
        return redirect('core:expert_dashboard')

    if request.method == 'POST':
        advice_bn = request.POST.get('advice_bn')
        if advice_bn:
            ExpertAdvice.objects.create(
                expert=expert_profile,
                diagnostic_record=record,
                advice_bn=advice_bn,
                advice_en=""
            )
            messages.success(request, "কৃষকের জন্য আপনার পরামর্শ সফলভাবে জমা হয়েছে।")
            return redirect('core:expert_dashboard')
        else:
            messages.error(request, "অনুগ্রহ করে একটি পরামর্শ লিখুন।")
        
    return render(request, 'experts/review_diagnosis.html', {'record': record})

@login_required
def edit_profile(request):
    profile, created = ExpertProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = ExpertUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = ExpertProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "আপনার প্রোফাইল সফলভাবে আপডেট করা হয়েছে।")
            return redirect('core:profile')
    else:
        user_form = ExpertUserForm(instance=request.user)
        profile_form = ExpertProfileForm(instance=profile)
        
    return render(request, 'profile/expert_edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def review_history(request):
    if request.user.role != 'expert':
        return redirect('core:index')
        
    expert_profile, _ = ExpertProfile.objects.get_or_create(user=request.user)
    
    # Get all advices provided by this expert, ordered by newest first
    advices = ExpertAdvice.objects.filter(expert=expert_profile).order_by('-created_at')
    
    return render(request, 'experts/review_history.html', {
        'advices': advices
    })
