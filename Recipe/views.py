from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredient, Tag, Step
from User.models import Favorite
from .forms import RecipeForm, IngredientFormSet, StepFormSet
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Count
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

def home_feed(request):
    recipes = Recipe.objects.filter(visibility=Recipe.PUBLIC, status='approved').order_by('-created_at')
    
    trending_recipes = Recipe.objects.filter(visibility=Recipe.PUBLIC, status='approved').annotate(
        num_favorites=Count('favorited_by')
    ).order_by('-num_favorites', '-created_at')[:5]

    # Advanced Search parameters
    query = request.GET.get('q', '').strip()
    tag_list = request.GET.getlist('tag')
    ingredient_list = request.GET.getlist('ingredient')

    if query:
        recipes = recipes.filter(title__icontains=query)
    
    tags = []
    for item in tag_list:
        tags.extend([t.strip() for t in item.split(',') if t.strip()])
    for tag in tags:
        recipes = recipes.filter(tags__name__icontains=tag)
        
    ingredients = []
    for item in ingredient_list:
        ingredients.extend([i.strip() for i in item.split(',') if i.strip()])
    for ingredient in ingredients:
        recipes = recipes.filter(ingredients__name__icontains=ingredient)

    # Avoid duplicate rows from joining ManyToMany filters
    recipes = recipes.distinct()

    # Pre-calculate user favorites to avoid N+1 queries in the template
    user_favorited_ids = []
    if request.user.is_authenticated:
        user_favorited_ids = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)

    # All tags for JS autocomplete
    all_tags = list(Tag.objects.values_list('name', flat=True).distinct())

    context = {
        'recipes': recipes,
        'trending_recipes': trending_recipes,
        'user_favorited_ids': list(user_favorited_ids),
        'q': query,
        'tag_search': ', '.join(tags),
        'ingredient_search': ', '.join(ingredients),
        'all_tags': all_tags,
    }
    return render(request, 'home_feed.html', context)


def search_recommendations(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q = request.GET.get('q', '').strip()
        if q:
            recipes = Recipe.objects.filter(visibility=Recipe.PUBLIC, status='approved', title__icontains=q).values_list('title', flat=True)[:5]
            return JsonResponse({'results': list(recipes)})
    return JsonResponse({'results': []})

def advanced_search(request):
    recipes = Recipe.objects.filter(visibility=Recipe.PUBLIC, status='approved').order_by('-created_at')

    # Advanced Search parameters
    query = request.GET.get('q', '').strip()
    tag_list = request.GET.getlist('tag')
    ingredient_list = request.GET.getlist('ingredient')

    if query:
        recipes = recipes.filter(title__icontains=query)
    
    tags = []
    for item in tag_list:
        tags.extend([t.strip() for t in item.split(',') if t.strip()])
    for tag in tags:
        recipes = recipes.filter(tags__name__icontains=tag)
        
    ingredients = []
    for item in ingredient_list:
        ingredients.extend([i.strip() for i in item.split(',') if i.strip()])
    for ingredient in ingredients:
        recipes = recipes.filter(ingredients__name__icontains=ingredient)

    recipes = recipes.distinct()

    # Pre-calculate user favorites to avoid N+1 queries in the template
    user_favorited_ids = []
    if request.user.is_authenticated:
        user_favorited_ids = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)

    all_tags = list(Tag.objects.values_list('name', flat=True).distinct())

    context = {
        'recipes': recipes,
        'user_favorited_ids': list(user_favorited_ids),
        'q': query,
        'tag_search': ', '.join(tags),
        'selected_tags': tags,
        'ingredient_search': ', '.join(ingredients),
        'all_tags': all_tags,
    }
    return render(request, 'advanced_search.html', context)



def create_recipe(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Main recipe form
            recipe_form = RecipeForm(request.POST, request.FILES)

            if recipe_form.is_valid():
                # Save recipe 
                recipe = recipe_form.save(commit=False)
                recipe.author = request.user
                
                # Only public recipes need admin approval. Private ones are automatically approved.
                if recipe.visibility == Recipe.PRIVATE:
                    recipe.status = 'approved'
                else:
                    recipe.status = 'pending'
                    
                recipe.save()

                # Handle tags
                tags_input = request.POST.getlist('tags')
                tag_objects = []

                for tag in tags_input:
                    tag = tag.strip()

                    if tag.isdigit():
                        tag_objects.append(Tag.objects.get(id=int(tag)))
                    else:
                        tag_obj, created = Tag.objects.get_or_create(
                            name__iexact=tag,
                            defaults={'name': tag}
                        )
                        if not created:
                            tag_obj = Tag.objects.get(name__iexact=tag)

                        tag_objects.append(tag_obj)

                recipe.tags.set(tag_objects)



                # -----------------------------
                # Ingredients Formset
                # -----------------------------
                ingredient_formset = IngredientFormSet(
                    request.POST,
                    instance=recipe,
                    prefix='ingredients'
                )

                # -----------------------------
                # Steps Formset
                # -----------------------------
                step_formset = StepFormSet(
                    request.POST,
                    request.FILES,
                    instance=recipe,
                    prefix='steps'
                )
        

                if ingredient_formset.is_valid() and step_formset.is_valid():
                    # Save formsets
                    ingredient_formset.save()
                    step_formset.save()

                    return redirect('recipe_detail', recipe.id)
                else:
                    # If formsets invalid, render with errors
                    pass

            else:
                # Recipe form invalid, render with errors
                ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.none(), prefix='ingredients')
                step_formset = StepFormSet(queryset=Step.objects.none(), prefix='steps')

        else:
            # GET request: empty forms
            recipe_form = RecipeForm()
            ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.none(), prefix='ingredients')
            step_formset = StepFormSet(queryset=Step.objects.none(), prefix='steps')

        popular_tags = Tag.objects.all()[:10]
    
    else:
        return redirect('login')

    return render(request, 'create_recipe.html', {
        'form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'popular_tags': popular_tags,
    })


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = recipe.ingredients.all() 
    steps = recipe.steps.all()
    context = {
        "recipe" : recipe,
        "ingredients" : ingredients,
        "steps" : steps,
    }
    return render(request, 'recipe_detail.html', context)

@login_required
def delete_ajax(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
        recipe.delete()

        return JsonResponse({
            "status": "success",
            "message" : "deleted recipe",
            "redirect_url": reverse('my_cookbooks')
        })
    return JsonResponse({
        "status" : "error",
        "message" : "Invalid request method"
    }, status=405)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    old_visibility = recipe.visibility
    
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)

        ingredient_formset = IngredientFormSet(
            request.POST,
            instance=recipe,
            prefix='ingredients'
        )

        step_formset = StepFormSet(
            request.POST,
            request.FILES,
            instance=recipe,    
            prefix='steps'
        )

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            edited_recipe = recipe_form.save(commit=False)
            
            # Workflow logic for approvals based on visibility
            if edited_recipe.visibility == Recipe.PRIVATE:
                edited_recipe.status = 'approved' # Private recipes don't need approval
            elif edited_recipe.visibility == Recipe.PUBLIC:
                edited_recipe.status = 'pending' # Any edit to a public recipe requires admin review
                
            edited_recipe.save()
            
            tags_input = request.POST.getlist('tags')
            tag_objects = []

            for tag in tags_input:
                tag = tag.strip()

                if tag.isdigit():
                    tag_objects.append(Tag.objects.get(id=int(tag)))
                else:
                    tag_obj, created = Tag.objects.get_or_create(
                        name__iexact=tag,
                        defaults={'name': tag}
                    )
                    if not created:
                        tag_obj = Tag.objects.get(name__iexact=tag)

                    tag_objects.append(tag_obj)

            recipe.tags.set(tag_objects)
            ingredient_formset.save()
            step_formset.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
        else:
            pass
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(instance=recipe, prefix='steps')

    existing_tag_ids = recipe.tags.values_list('id', flat=True)
    popular_tags = Tag.objects.all()[:10]
    return render(request, 'edit_recipe.html', {
    'form': recipe_form,
    'ingredient_formset': ingredient_formset,
    'step_formset': step_formset,
    'popular_tags': popular_tags,
    'existing_tag_ids': existing_tag_ids,
    'recipe':recipe,
    'steps':recipe.steps.all()

})

@login_required
def nutrition_analysis(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # URL for guessNutrition
    url = f"https://api.spoonacular.com/recipes/guessNutrition?title={recipe.title}&apiKey={SPOONACULAR_API_KEY}"
    
    # Mock data fallback
    nutrition_data = {
        "calories": {"value": 450, "unit": "kcal"},
        "fat": {"value": 15, "unit": "g"},
        "protein": {"value": 20, "unit": "g"},
        "carbs": {"value": 50, "unit": "g"},
        "status": "Using Mock Data - Configure SPOONACULAR_API_KEY in .env"
    }
    
    if SPOONACULAR_API_KEY and SPOONACULAR_API_KEY != "your_actual_key_here":
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Spoonacular guessNutrition returns data in a slightly different format
                # We normalize it for our front end
                nutrition_data = {
                    "calories": data.get("calories", {"value": 0, "unit": "kcal"}),
                    "fat": data.get("fat", {"value": 0, "unit": "g"}),
                    "protein": data.get("protein", {"value": 0, "unit": "g"}),
                    "carbs": data.get("carbs", {"value": 0, "unit": "g"}),
                    "status": "Real-time API Data"
                }
            else:
                nutrition_data["status"] = f"API Error: {response.status_code}"
        except Exception as e:
            nutrition_data["status"] = f"Connection Error: {str(e)}"

    return JsonResponse(nutrition_data)

@login_required
def ingredient_substitute(request, ingredient_name):
    url = f"https://api.spoonacular.com/food/ingredients/substitutes?ingredientName={ingredient_name}&apiKey={SPOONACULAR_API_KEY}"
    
    substitutes = {
        "status": "success", 
        "substitutes": [f"Option 1 for {ingredient_name}", f"Option 2 for {ingredient_name}"], 
        "message": "Using mock data - Configure SPOONACULAR_API_KEY in .env"
    }
    
    if SPOONACULAR_API_KEY and SPOONACULAR_API_KEY != "your_actual_key_here":
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                substitutes = response.json()
            else:
                substitutes["message"] = f"API Error: {response.status_code}"
        except Exception as e:
            substitutes["message"] = f"Connection Error: {str(e)}"
        
    return JsonResponse(substitutes)


def download_recipe_pdf(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    template_path = 'recipe_pdf.html'
    context = {
        'recipe': recipe,
        'ingredients': recipe.ingredients.all(),
        'steps': recipe.steps.all(),
    }
    
    response = HttpResponse(content_type='application/pdf')
    # Safe filename formatting
    safe_filename = "".join([c for c in recipe.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    response['Content-Disposition'] = f'attachment; filename="{safe_filename.replace(" ", "_")}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
