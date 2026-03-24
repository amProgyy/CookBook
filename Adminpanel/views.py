from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from Recipe.models import Recipe, Tag
from User.models import Notification

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_dashboard')
    return redirect('login')

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    pending_recipes = Recipe.objects.filter(visibility=Recipe.PUBLIC, status='pending').order_by('-created_at')

    context = {
        'pending_recipes': pending_recipes,
    }
    return render(request, 'Adminpanel/admin_dashboard.html', context)

@user_passes_test(is_admin, login_url='login')
def manage_users(request):
    user_search = request.GET.get('user_search', '').strip()
    
    all_users = User.objects.all().order_by('-date_joined')
    if user_search:
        all_users = all_users.filter(username__icontains=user_search) | all_users.filter(email__icontains=user_search)
        
    context = {
        'all_users': all_users.distinct(),
        'user_search': user_search,
    }
    return render(request, 'Adminpanel/admin_users.html', context)

@user_passes_test(is_admin, login_url='login')
def manage_recipes(request):
    recipe_search = request.GET.get('recipe_search', '').strip()

    all_recipes = Recipe.objects.all().order_by('-created_at')
    if recipe_search:
        all_recipes = all_recipes.filter(title__icontains=recipe_search) | all_recipes.filter(author__username__icontains=recipe_search)

    all_tags = Tag.objects.all().order_by('name')

    context = {
        'all_recipes': all_recipes.distinct(),
        'recipe_search': recipe_search,
        'all_tags': all_tags,
    }
    return render(request, 'Adminpanel/admin_recipes.html', context)

@user_passes_test(is_admin, login_url='login')
def approve_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        recipe.status = 'approved'
        recipe.save()
        Notification.objects.create(
            user=recipe.author,
            recipe=recipe,
            message=f"Your recipe '{recipe.title}' has been approved!"
        )
        messages.success(request, f'Recipe "{recipe.title}" has been approved.')
    return redirect('admin_dashboard')

@user_passes_test(is_admin, login_url='login')
def reject_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        reason = request.POST.get('rejection_reason', '')
        recipe.status = 'rejected'
        recipe.rejection_reason = reason
        recipe.save()
        Notification.objects.create(
            user=recipe.author,
            recipe=recipe,
            message=f"Your recipe '{recipe.title}' was rejected. Reason: {reason if reason else 'No specific reason provided.'}"
        )
    messages.success(request, f'Recipe "{recipe.title}" has been rejected.')
    return redirect('admin_dashboard')

@user_passes_test(is_admin, login_url='login')
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        Notification.objects.create(
            user=recipe.author,
            message=f"Your recipe '{recipe.title}' was deleted by an administrator."
        )
        recipe.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Recipe deleted successfully.'})
        messages.success(request, f'Recipe deleted successfully.')
    return redirect('manage_recipes')

@user_passes_test(is_admin, login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Ensure superuser doesn't easily delete themselves immediately, but okay let's allow admins
    if request.method == "POST":
        if user == request.user:
            messages.error(request, 'You cannot delete yourself!')
        else:
            user.delete()
            messages.success(request, f'User {user.username} deleted successfully.')
    return redirect('manage_users')

@user_passes_test(is_admin, login_url='login')
def add_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get('tag_name', '').strip()
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'tag_id': tag.id, 'tag_name': tag.name, 'message': f'Tag "{tag.name}" added successfully.'})
                messages.success(request, f'Tag "{tag.name}" added successfully.')
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': f'Tag "{tag_name}" already exists.'})
                messages.error(request, f'Tag "{tag_name}" already exists.')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Tag name cannot be empty.'})
    return redirect('manage_recipes')

@user_passes_test(is_admin, login_url='login')
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == "POST":
        tag_name = tag.name
        tag.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'Tag "{tag_name}" deleted successfully.'})
        messages.success(request, f'Tag "{tag_name}" deleted successfully.')
    return redirect('manage_recipes')
