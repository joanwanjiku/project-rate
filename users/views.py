from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from projects.models import Post

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created')
            return redirect('login')
    else:
        form = SignUpForm()
       
    return render(request, 'users/register.html',{'form': form} )


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(user=user.id)
    if request.method == 'POST':
        up_form = UserUpdateForm(request.POST, instance=request.user)
        pr_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if up_form.is_valid() and pr_form.is_valid():
            up_form.save()
            pr_form.save()
            messages.success(request, f'Account has been updated')
            return redirect('profile')
    else:
        up_form = UserUpdateForm(instance=request.user)
        pr_form = ProfileUpdateForm(instance=request.user.profile)
    content = {
        'user_form': up_form,
        'profile_form': pr_form,
        'posts': posts
    }
    return render(request, 'users/profile.html', content)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


