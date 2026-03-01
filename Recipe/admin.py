from django.contrib import admin
from .models import Recipe, Tag, Ingredient, Step
from User.models import Notification

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'visibility', 'created_at')
    list_filter = ('status', 'visibility')
    search_fields = ('title', 'author__username')
    
    def save_model(self, request, obj, form, change):
        # Trigger notification only if the status changed
        if change:
            old_obj = Recipe.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                if obj.status == 'approved':
                    Notification.objects.create(
                        user=obj.author,
                        recipe=obj,
                        message=f"Your recipe '{obj.title}' has been approved!"
                    )
                elif obj.status == 'rejected':
                    reason = obj.rejection_reason if obj.rejection_reason else "No specific reason provided."
                    Notification.objects.create(
                        user=obj.author,
                        recipe=obj,
                        message=f"Your recipe '{obj.title}' was rejected. Reason: {reason}"
                    )
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        # Notify before deleting because the user reference might be lost if CASCADE but user is not deleted
        # Wait, if admin deletes *recipe*, user still exists.
        Notification.objects.create(
            user=obj.author,
            message=f"Your recipe '{obj.title}' was deleted by an administrator."
        )
        super().delete_model(request, obj)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Step)
