from django.contrib import admin

from vista_med.models import (
    Action, ActionType, Employee, Event, EventType, FinancingSource, Organisation, OrganisationStructure, Patient, Visit
)


class ReadOnlyModelAdmin(admin.ModelAdmin):
    """
    ModelAdmin class that prevents modifications through the admin.
    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    Source: https://gist.github.com/aaugustin/1388243
    """

    actions = None

    # We cannot call super().get_fields(request, obj) because that method calls
    # get_readonly_fields(request, obj), causing infinite recursion. Ditto for
    # super().get_form(request, obj). So we  assume the default ModelForm.
    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def get_list_display(self, request, obj=None):
        return self.get_readonly_fields(request, obj)

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them.
    def has_change_permission(self, request, obj=None):
        return request.method in ["GET", "HEAD"] and super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Visit, ReadOnlyModelAdmin)
admin.site.register(Patient, ReadOnlyModelAdmin)
admin.site.register(Action, ReadOnlyModelAdmin)
admin.site.register(ActionType, ReadOnlyModelAdmin)
admin.site.register(Event, ReadOnlyModelAdmin)
admin.site.register(EventType, ReadOnlyModelAdmin)
admin.site.register(Employee, ReadOnlyModelAdmin)
admin.site.register(Organisation, ReadOnlyModelAdmin)
admin.site.register(OrganisationStructure, ReadOnlyModelAdmin)
admin.site.register(FinancingSource, ReadOnlyModelAdmin)
