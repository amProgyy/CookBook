from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredient, Tag, Step
from .forms import RecipeForm, IngredientFormSet, StepFormSet
from decimal import Decimal, ROUND_HALF_UP

@login_required
def create_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormSet(
            request.POST,
            queryset=Ingredient.objects.none(), prefix='ingredients'
        )
        step_formset = StepFormSet(
            request.POST,
            queryset=Step.objects.none(), prefix='steps'
        )

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            # Save recipe
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Handle tags
            tag_string = recipe_form.cleaned_data.get('tag_names')
            if tag_string:
                tag_list = [
                    t.strip().lower()
                    for t in tag_string.split(',')
                    if t.strip()
                ]
                for tag_name in tag_list:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    recipe.tags.add(tag)

            # Save ingredients
            for form in ingredient_formset:
                if form.cleaned_data:
                    ingredient = form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            # Save steps
            for form in step_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step = form.save(commit=False)
                    step.recipe = recipe
                    step.save()  # step_number auto-filled in model's save()

            return redirect('recipe_detail', recipe.id)

    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.none(), prefix='ingredients')
        step_formset = StepFormSet(queryset=Step.objects.none(), prefix='steps')

    return render(request, 'create_recipe.html', {
        'form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset
    })

@login_required
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






