from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from Recipe.models import Recipe
from User.models import Favorite, Notification



def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(
                    username=username, 
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                    )
                login(request, user)
                return redirect('home_feed')
    else:
        return redirect('home_feed')
        
    return render(request, 'signup.html')



def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username does not exist")
                return render(request, "login.html")

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Incorrect password")
            else:
                login(request, user)
                if user.is_staff or user.is_superuser:
                    return redirect("admin_dashboard")
                return redirect("home_feed")
    else:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home_feed')
        
    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('home_feed')
            

@login_required
def my_cookbooks(request):
    user = request.user
    
    # Sort recipes by newest first and separate by their visibility status
    public_recipes = user.recipes.filter(visibility=Recipe.PUBLIC).order_by('-created_at')
    private_recipes = user.recipes.filter(visibility=Recipe.PRIVATE).order_by('-created_at')

    context = {
        "public_recipes": public_recipes,
        "private_recipes": private_recipes,
        "is_favorites_page": False
    }
    return render(request, "my_cookbooks.html", context)
                

    
@login_required
def toggle_favorite(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)

        if not created:
            # It already existed, meaning user wants to UN-favorite it
            favorite.delete()
            return JsonResponse({'status': 'unfavorited'})
        
        return JsonResponse({'status': 'favorited'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def favorite_recipes(request):
    # Get all recipes favorited by the current user
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    recipes = [fav.recipe for fav in favorites]
    
    context = {
        "recipes": recipes,
        "is_favorites_page": True
    }
    return render(request, "my_cookbooks.html", context)


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # Public & Approved recipes by the user
    user_recipes = Recipe.objects.filter(author=profile_user, visibility=Recipe.PUBLIC, status='approved')
    
    # User's favorite recipes (only public & approved ones)
    favorites = Favorite.objects.filter(user=profile_user).select_related('recipe')
    favorite_recipes = [fav.recipe for fav in favorites if fav.recipe.visibility == Recipe.PUBLIC and fav.recipe.status == 'approved']
    
    user_favorited_ids = []
    if request.user.is_authenticated:
        user_favorited_ids = list(Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True))

    context = {
        'profile_user': profile_user,
        'user_recipes': user_recipes,
        'favorite_recipes': favorite_recipes,
        'user_favorited_ids': user_favorited_ids,
    }
    return render(request, 'user_profile.html', context)

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {'notifications': notifications}
    
    # Render before marking as read if we want to distinguish new vs old visually
    # But let's just mark them as read right away.
    notifications.update(is_read=True)
    return render(request, 'notifications.html', context)
