from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple 
from django.contrib.auth.models import User as djangouser, Group as djangogroup
from django.contrib.sites.models import Site as djangosite


#customized module
import models
import admin_ip, admin_user, admin_auth

#admin.site.unregister(djangouser)
#admin.site.unregister(djangogroup)
#admin.site.unregister(djangosite)

from models import *




class TemplatesForm(forms.ModelForm):
    class Meta:
        model = templates
    ips = forms.ModelMultipleChoiceField(
        queryset=IP.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name= ('Ip list'),
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(TemplatesForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['ips'].initial = self.instance.ip_set.all()

    def save(self, commit=True):
        groupmachine = super(TemplatesForm, self).save(commit=False)  
        if commit:
            groupmachine.save()
        if groupmachine.pk:
            groupmachine.ip_set = self.cleaned_data['ips']
            self.save_m2m()
        return groupmachine


class TemplatesAdmin(admin.ModelAdmin):
	form = TemplatesForm

    #list_display = ('name',)

    #filter_horizontal = ('service_list','groups','hosts','graph_list')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'monitor_type','check_interval')
    filter_horizontal = ('item_list',)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name','key','data_type','enabled')


class TriggersAdmin(admin.ModelAdmin):
	list_display = ('name',)
class QuickLinkAdmin(admin.ModelAdmin):
	list_display = ('link_name','url','color')
#class GroupAdmin(admin.ModelAdmin):
#    form = GroupForm
admin.site.register(Idc)
admin.site.register(IP, admin_ip.IpAdmin)
admin.site.register(Group, admin_ip.GroupAdmin)
admin.site.register(RemoteUser, admin_user.RemoteUserAdmin)
admin.site.register(TriaquaeUser, admin_user.TriaquaeUserAdmin)
admin.site.register(AuthByIpAndRemoteUser, admin_auth.AuthByIpAndRemoteUserAdmin)


admin.site.register(templates,TemplatesAdmin)
admin.site.register(services,ServicesAdmin)
admin.site.register(items,ItemsAdmin)
admin.site.register(triggers,TriggersAdmin)
admin.site.register(graphs)
admin.site.register(operations)
admin.site.register(conditions)
admin.site.register(actions)
admin.site.register(trunk_servers)

