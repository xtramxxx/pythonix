__author__ = 'Jeka'
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseForbidden
from django.contrib.auth.models import User

import app_admin.models as app_admin_models


class BaseAdminContentMixin(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            ca = app_admin_models.AdminProfile.objects.get(id=self.request.user.id)
        except:
            if User.objects.get(id=self.request.user.id).is_superuser == False:
                return HttpResponseForbidden()
        return super(BaseAdminContentMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseAdminContentMixin, self).get_context_data(**kwargs)
        context['access_clients_groups'] = app_admin_models.ClientsGroups.objects.filter(select_admin=self.request.user)
        context['clients_count'] = app_admin_models.Clients.objects.all().count()
        return context


