from django.shortcuts import render,redirect
from .models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed

CustomUser = get_user_model()  # Get the custom user model

# View function for user registration
def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        referral_code = request.POST.get('referral_code')

        try:
            # Create the user instance with required fields
            user = CustomUser.objects.create_user(username=email, email=email, password=password)

            # Set the user's name
            user.name = name
            user.save()

            # Set referral code if provided
            if referral_code:
                user.referral_code = referral_code
                user.save()

                # Logic to award points to referring user
                referring_user = CustomUser.objects.filter(referral_code=referral_code).first()
                if referring_user:
                    referring_user.points += 1
                    referring_user.save()

            # Authenticate and login the user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to registration success page with user ID
                return redirect('registration_success', user_id=user.id)
            else:
                raise IntegrityError("Failed to authenticate user.")

        except IntegrityError:
            error_message = "Email already exists. Please use a different email."
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')

# View function for registration success page
def registration_success(request, user_id):
    return render(request, 'registration_success.html', {'user_id': user_id})

# View function to display user details
@login_required
def user_details(request):
    if request.method == 'GET':
        user = request.user
        referral_code = None  # Default value
        
        # Check if the user has a related profile with referral code
        if hasattr(user, 'profile') and user.profile.referral_code:
            referral_code = user.profile.referral_code
        
        context = {
            'name': user.username,
            'email': user.email,
            'referral_code': referral_code,
            'registration_timestamp': user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return render(request, 'user_details.html', context)
    else:
        # Return method not allowed for other HTTP methods
        return render(request, 'method_not_allowed.html', status=405)
    
    
# View function for displaying user referrals    
@login_required
def referrals_endpoint(request):
    if request.method == 'GET':
        # Retrieve the current user
        current_user = request.user
        
        # Check if the current user has a referral code
        if hasattr(current_user, 'referral_code'):
            # Retrieve the users who registered using the current user's referral code
            referred_users = User.objects.filter(referral_code=current_user.referral_code)
            
            # Implement pagination
            paginator = Paginator(referred_users, 20)  # 20 users per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            # Pass the paginated referrals to the template
            return render(request, 'referrals.html', {'page_obj': page_obj})
        else:
            message = 'You do not have a referral code.'
            return render(request, 'referrals.html', {'message': message})
    else:
        return HttpResponseNotAllowed(['GET'])
