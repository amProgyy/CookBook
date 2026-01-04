from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    chefs_note = models.TextField(blank=True)
    number_of_servings = models.PositiveIntegerField()

    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Ingredient(models.Model):

    UNIT_CHOICES = [
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('ml', 'Milliliter'),
        ('l', 'Liter'),
        ('tsp', 'Teaspoon'),
        ('tbsp', 'Tablespoon'),
        ('cup', 'Cup'),
        ('pcs', 'Pieces'),
    ]

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    class Meta:
        unique_together = ('recipe', 'name')
        ordering = ['id']


class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()

    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')

   

    def save(self, *args, **kwargs):
        if not self.step_number:
            # Get the current maximum step number for this recipe
            max_step = Step.objects.filter(recipe=self.recipe).aggregate(
                Max('step_number')
            )['step_number__max'] or 0
            self.step_number = max_step + 1
        super().save(*args, **kwargs)


