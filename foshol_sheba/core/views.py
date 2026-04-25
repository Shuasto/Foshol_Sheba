from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dotenv import load_dotenv
from core.models import User, DiagnosticHistory, MarketPrice, CommunityPost, Crop, Disease, Comment
from core.services.badge_service import get_user_badges
import os
import uuid

load_dotenv()
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def dashboard(request):
    if request.user.role == 'farmer':
        return redirect('farmers:dashboard')
    elif request.user.role == 'expert':
        return expert_dashboard(request)
    elif request.user.role == 'company':
        return company_dashboard(request)
    return render(request, 'dashboard.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
        
    if request.method == 'POST':
        login_input = request.POST.get('username')  # This matches the 'name' attribute in HTML
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Check if login_input is an email or username
        if '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                username = user_obj.username
            except User.DoesNotExist:
                username = login_input  # Let authenticate fail naturally
        else:
            username = login_input

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if remember:
                # Set session to expire in 2 weeks
                request.session.set_expiry(int(os.getenv('SESSION_COOKIE_AGE', 1209600)))
            else:
                # Set session to expire on browser close
                request.session.set_expiry(0)
                
            messages.success(request, f"স্বাগতম, {user.first_name}! আপনি সফলভাবে লগ ইন করেছেন।")
            return redirect('core:dashboard')
        else:
            messages.error(request, "ইউজারনেম বা পাসওয়ার্ড সঠিক নয়।")
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "আপনি সফলভাবে লগ আউট করেছেন।")
    return redirect('core:login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = request.POST.get('full_name')  # For company
        phone_no = request.POST.get('phone_no')
        district = request.POST.get('district')
        upazila = request.POST.get('upazila')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        # Basic Validation
            
        if password != confirm_password:
            messages.error(request, "পাসওয়ার্ড দুটি মেলেনি।")
            return render(request, 'register.html')

        try:
            # Generate Username
            if role == 'company':
                base_name = full_name
                final_first_name = full_name
                final_last_name = ""
            else:
                base_name = f"{first_name}_{last_name}"
                final_first_name = first_name
                final_last_name = last_name
            
            # Clean name: spaces -> _, remove dots, lowercase
            clean_name = base_name.strip().replace(' ', '_').replace('.', '').lower()
            unique_id = str(uuid.uuid4())[:8]
            generated_username = f"{clean_name}_{unique_id}_{role}"

            # Handle Email (Demo if empty)
            if not email:
                email = f"{generated_username}@demo.com"
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "এই ইমেইলটি ইতিপূর্বে ব্যবহার করা হয়েছে।")
                    return render(request, 'register.html')

            # Phone Number Validation (Unique check)
            if phone_no:
                if User.objects.filter(phone_no=phone_no).exists():
                    messages.error(request, "এই মোবাইল নম্বরটি ইতিপূর্বে নিবন্ধন করা হয়েছে।")
                    return render(request, 'register.html')

            user = User.objects.create_user(
                username=generated_username,
                email=email,
                password=password,
                role=role,
                first_name=final_first_name,
                last_name=final_last_name,
                phone_no=phone_no,
                district=district,
                upazila=upazila,
                address=address
            )
            
            if profile_picture:
                # Save the image as username.png
                profile_picture.name = f"{generated_username}.png"
                user.profile_picture = profile_picture
                user.save()
                
            messages.success(request, "আপনার অ্যাকাউন্টটি সফলভাবে তৈরি করা হয়েছে! আপনি এখন লগ ইন করতে পারেন।")
            return redirect('core:login')
            
        except Exception as e:
            messages.error(request, f"নিবন্ধন করার সময় একটি ত্রুটি হয়েছে: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')

@login_required
def farmer_dashboard_redirect(request):
    return redirect('farmers:dashboard')

def market_prices(request):
    query = request.GET.get('q', '')
    prices = MarketPrice.objects.all()
    
    if query:
        prices = prices.filter(
            models.Q(crop__name_en__icontains=query) | 
            models.Q(crop__name_bn__icontains=query) |
            models.Q(market_name__icontains=query)
        )
        
    prices = prices.order_by('-updated_at')
    return render(request, 'core/marketprice_full_view.html', {
        'prices': prices,
        'query': query
    })

def forum_list(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    return render(request, 'forum/list.html', {'posts': posts})

@login_required
def my_forum_posts(request):
    posts = CommunityPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'forum/list.html', {'posts': posts, 'is_my_posts': True})

def forum_detail(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            messages.success(request, "আপনার মন্তব্যটি সফলভাবে যুক্ত করা হয়েছে!")
            return redirect('core:forum_detail', pk=pk)
            
    author_badges = get_user_badges(post.user)
    return render(request, 'forum/detail.html', {
        'post': post,
        'author_badges': author_badges
    })

@login_required
def forum_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        diagnosis_id = request.POST.get('diagnosis_id')
        
        post = CommunityPost.objects.create(
            user=request.user,
            title=title,
            content=content,
            image=image
        )
        
        if diagnosis_id:
            try:
                diagnosis = DiagnosticHistory.objects.get(pk=diagnosis_id, user=request.user)
                post.related_diagnosis = diagnosis
                post.save()
            except DiagnosticHistory.DoesNotExist:
                pass
                
        messages.success(request, "আপনার পোস্টটি সফলভাবে ফোরামে যুক্ত করা হয়েছে!")
        return redirect('core:forum_detail', pk=post.pk)
        
    # Handle GET request with optional diagnosis_id to pre-fill
    diagnosis_id = request.GET.get('diagnosis_id')
    diagnosis = None
    initial_title = ""
    initial_content = ""
    
    if diagnosis_id:
        try:
            diagnosis = DiagnosticHistory.objects.get(pk=diagnosis_id, user=request.user)
            # Pre-fill title: Crop: Disease
            crop_name = diagnosis.crop.name_bn if diagnosis.crop else "অজানা ফসল"
            disease_name = diagnosis.detected_disease.name_bn if diagnosis.detected_disease else "সমস্যা বিশ্লেষণ"
            initial_title = f"{crop_name}: {disease_name}"
            # Pre-fill content with AI generated description if available
            initial_content = diagnosis.ai_description if diagnosis.ai_description else ""
        except DiagnosticHistory.DoesNotExist:
            pass
            
    return render(request, 'forum/create.html', {
        'diagnosis': diagnosis,
        'initial_title': initial_title,
        'initial_content': initial_content
    })

def product_list(request):
    from pesticide_companies.models import Product
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products})

@login_required
def expert_dashboard(request):
    from experts.models import ExpertProfile, ExpertAdvice
    expert_profile, _ = ExpertProfile.objects.get_or_create(user=request.user)
    
    pending_verifications = DiagnosticHistory.objects.filter(
        expert_advices__isnull=True, 
        status='completed'
    ).order_by('-created_at')[:10]
    
    my_advices_count = ExpertAdvice.objects.filter(expert=expert_profile).count()
    
    is_profile_incomplete = not expert_profile.specialization or not expert_profile.qualification
    
    return render(request, 'dashboards/expert.html', {
        'pending_tasks': pending_verifications,
        'profile': expert_profile,
        'my_advices_count': my_advices_count,
        'is_profile_incomplete': is_profile_incomplete
    })

@login_required
def company_dashboard(request):
    my_products = request.user.products.all()
    return render(request, 'dashboards/company.html', {
        'products': my_products
    })

@login_required
def profile_view(request):
    if request.user.role == 'farmer':
        return redirect('farmers:profile')
    elif request.user.role == 'expert':
        from experts.models import ExpertProfile
        profile, created = ExpertProfile.objects.get_or_create(user=request.user)
        return render(request, 'profile/expert_profile.html', {
            'profile': profile,
            'user': request.user
        })
    elif request.user.role == 'company':
        return render(request, 'profile/company_profile.html', {
            'user': request.user
        })
    
    # Fallback for admin or other roles
    return render(request, 'dashboard.html')

def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'core/crop_list.html', {'crops': crops})

def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    diseases = crop.diseases.all()
    return render(request, 'core/crop_detail.html', {
        'crop': crop,
        'diseases': diseases
    })

def disease_list(request):
    query = request.GET.get('q', '')
    diseases = Disease.objects.all()
    if query:
        diseases = diseases.filter(
            models.Q(name_en__icontains=query) |
            models.Q(name_bn__icontains=query) |
            models.Q(crop__name_bn__icontains=query)
        )
    return render(request, 'core/disease_list.html', {
        'diseases': diseases,
        'query': query
    })

def disease_detail(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    return render(request, 'core/disease_detail.html', {'disease': disease})

def expert_directory(request):
    from experts.models import ExpertProfile
    experts = ExpertProfile.objects.filter(is_verified_by_admin=True).select_related('user')
    return render(request, 'core/expert_directory.html', {'experts': experts})
