from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Recipe.models import Recipe



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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist")
            return render(request, "login.html")

        user = User.objects.get(username=username, password=password)

        if user is None:
            messages.error(request, "Incorrect password")
        else:
            login(request, user)
            return redirect("create_recipe")

    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
            

@login_required
def my_cookbooks(request):
    user = request.user
    recipes = user.recipes.all()
    # ingredients = user.ingredients.all()
    # # steps = user.steps.all()

    context = {
        "recipes" : recipes,
        
    }
    return render(request, "my_cookbooks.html", context)
                

    
