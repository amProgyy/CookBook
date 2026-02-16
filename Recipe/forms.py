from django import forms
from .models import Recipe, Ingredient, Step,Tag
from django.forms import inlineformset_factory

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'image',
            'title',
            'description',
            'chefs_note',
            'number_of_servings',
            'visibility',
            
        ]
        exclude = ['tags'] 
        widgets = {
        'title': forms.TextInput(attrs={
            'placeholder': 'Recipe Title',
            'class': 'recipe-title'
        }),

        'description': forms.Textarea(attrs={
            'rows': 3,
            'class': 'recipe-description',
            'placeholder': 'Brief description of the recipe'
        }),

        'chefs_note': forms.Textarea(attrs={
            'rows': 3,
            'placeholder': "write a secret tip",
            'class': 'chef-notes'
        }),
        'number_of_servings': forms.NumberInput(attrs={
                'min': 1,
                'class': 'servings-input'
            }),
        'image': forms.ClearableFileInput(attrs={
                'class': 'image-input',
                'accept': 'image/*'
            })
    }






class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingredient (e.g. Onion)',
                'class': 'ingredient-name'
            }),
            'quantity': forms.NumberInput(attrs={
                'placeholder': 'Qty',
                'step': '0.01',
                'class': 'ingredient-quantity'
            }),
            'unit': forms.Select(attrs={
                'class': 'ingredient-unit',
                'placeholder': 'Unit'
            }),
        }

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True
)



class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['instruction', 'image']  # step_number handled automatically
        widgets = {
            'instruction': forms.Textarea(attrs={
                'placeholder': 'Describe this step...',
                'rows': 2,
                'class': 'step-instruction'
            }),
        }


StepFormSet = inlineformset_factory(
    Recipe,
    Step,
    form=StepForm,
    extra=1,
    can_delete=True
)
