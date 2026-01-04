from django import forms
from .models import Recipe, Ingredient, Step
from django.forms import modelformset_factory

class RecipeForm(forms.ModelForm):
    tag_names = forms.CharField(
        required=False,
        label="Tags",
        help_text="Enter tags separated by commas (e.g. spicy, vegan, quick)",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'spicy, vegan, quick'
            }
        )
    )

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'chefs_note',
            'number_of_servings',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'chefs_note': forms.Textarea(attrs={'rows': 3}),
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
                'placeholder': 'Unit',
                'class': 'ingredient-unit'
            }),
        }

IngredientFormSet = modelformset_factory(
    Ingredient,
    form=IngredientForm,
     fields=('name', 'quantity', 'unit'),
    extra=1,
    can_delete=True
)




class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['instruction']  # step_number handled automatically
        widgets = {
            'instruction': forms.Textarea(attrs={
                'placeholder': 'Describe this step...',
                'rows': 2,
                'class': 'step-instruction'
            }),
        }


StepFormSet = modelformset_factory(
    Step,
    form=StepForm,
    extra=1,
    can_delete=True
)
