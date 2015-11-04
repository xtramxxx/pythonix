from django.contrib import admin
import app_admin.models


class TarifsModelAdmin(admin.ModelAdmin):
    model = app_admin.models.Tarifs

    def get_actions(self, request):
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(app_admin.models.AdminProfile)
admin.site.register(app_admin.models.PhysicalNetwork)
admin.site.register(app_admin.models.Servers)
admin.site.register(app_admin.models.IPV4Networks)
admin.site.register(app_admin.models.ClientsGroups)
admin.site.register(app_admin.models.Tarifs, TarifsModelAdmin)
admin.site.register(app_admin.models.Streets)
admin.site.register(app_admin.models.Clients)
admin.site.register(app_admin.models.ReportPayAdmin)
admin.site.register(app_admin.models.Employees)
admin.site.register(app_admin.models.Card)