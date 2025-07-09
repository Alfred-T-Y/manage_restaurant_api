from django.contrib import admin
from .models import (User, Owner, Manager, KitchenManager,
                     Deliver, Waiter)


class OwnerAdmin(admin.ModelAdmin):
    #for one object
    def delete_model(self, request, obj):
        # Appelle ta logique de suppression personnalisée
        obj.delete()
    #for many objects
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

# Register your models here.
admin.site.register(User)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Manager)
admin.site.register(KitchenManager)
admin.site.register(Waiter)
admin.site.register(Deliver)