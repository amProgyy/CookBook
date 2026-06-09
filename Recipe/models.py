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
    number_of_servings = models.PositiveIntegerField(default=1)
    servings_unit = models.CharField(max_length=50, default='persons')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PUBLIC = 'public'
    PRIVATE = 'private'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default=PUBLIC
    )

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    rejection_reason = models.TextField(blank=True)





class Ingredient(models.Model):

    UNIT_CHOICES = [
        ('', 'Select Unit'),
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
        ordering = ['id']


class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()

    image = models.ImageField(
    upload_to='steps/',
    blank=True,
    null=True
)

    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')

   

    def save(self, *args, **kwargs):
        # Auto-assign step number if not provided
        if not self.step_number:
            max_step = Step.objects.filter(recipe=self.recipe).aggregate(Max('step_number'))['step_number__max'] or 0
            self.step_number = max_step + 1
        super().save(*args, **kwargs)

        # Optional: renumber all steps to prevent gaps
        steps = Step.objects.filter(recipe=self.recipe).order_by('step_number')
        for idx, step in enumerate(steps, start=1):
            if step.step_number != idx:
                step.step_number = idx
                step.save(update_fields=['step_number'])

