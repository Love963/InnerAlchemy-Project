from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms  import UserRegistrationForm
from .forms import UserProfileForm
from django.contrib import messages

# DRF imports for AI views
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

# Web Views 
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def profile_update_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})


# API Views 
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True  # PATCH requests allowed
        return super().get_serializer(*args, **kwargs)


class UserListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
