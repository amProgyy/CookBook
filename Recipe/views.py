from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredient, Tag, Step
from .forms import RecipeForm, IngredientFormSet, StepFormSet
from decimal import Decimal, ROUND_HALF_UP


@login_required
def create_recipe(request):
    if request.method == 'POST':
        # Main recipe form
        recipe_form = RecipeForm(request.POST, request.FILES)

        if recipe_form.is_valid():
            # Save recipe 
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
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

    return render(request, 'create_recipe.html', {
        'form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'popular_tags': popular_tags,
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

@login_required
def delete_ajax(request, recipe_id):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
        recipe.delete()

        return JsonResponse({
            "status": "success",
            "message" : "deleted recipe",
            "redirect_url": "/user/my_cookbook/"
        })
    return JsonResponse({
        "status" : "not success",
        "message" : "failed to delte"
    })

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
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
            recipe_form.save()
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









