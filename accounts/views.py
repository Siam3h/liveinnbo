from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from .utils import generate_jwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import ProfileUpdateForm 
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Handles user login via both form and social auth."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = generate_jwt(user)  
            return redirect('user_admin')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login') 

    return render(request, 'accounts/login.html')


def social_auth_complete(request):
    """Handles post-social authentication."""
    user = request.user
    if user.is_authenticated:
        token = generate_jwt(user)  
        return redirect('accounts/user_admin_interface.html')
    return JsonResponse({'error': 'Authentication failed'}, status=400)

def protected_view(request):
    """Example of a protected view that requires OAuth authentication."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    return JsonResponse({'message': 'Success! You are authenticated.'})


def logout_view(request):
    """Logs out the user."""
    logout(request)
    return JsonResponse({'message': 'Successfully logged out.'}, status=200)


@login_required
def user_admin_interface(request):
    user = request.user
    return render(request, 'accounts/user_admin_interface.html', {'user': user})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})
