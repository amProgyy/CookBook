from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create(
                username=username, 
                first_name=first_name,
                last_name=last_name,
                password=password
                )
            login(request, user)
            return redirect('login')
        
    return render(request, 'signup.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # user = authenticate(request, username=username, password=password)
        user = User.objects.get(username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect username or password ")
        else:
            login(request, user)
            return redirect('create_recipe')

    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
            
                

    
