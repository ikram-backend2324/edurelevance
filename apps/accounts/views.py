from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('subjects:list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Xush kelibsiz! Ro'yxatdan o'tish muvaffaqiyatli.")
            return redirect('subjects:list')
        else:
            messages.error(request, "Xato yuz berdi. Iltimos qaytadan urinib ko'ring.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('subjects:list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            next_url = request.GET.get('next', 'subjects:list')
            return redirect(next_url)
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect('accounts:login')
