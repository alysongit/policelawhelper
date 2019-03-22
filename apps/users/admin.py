import xadmin
from apps.admin import BaseAdmin
from django.contrib.auth.models import User
from users.models import PoliceGroup, Police, PoliceType, Account


class PoliceGroupAdmin(BaseAdmin):
    model_icon = 'fa fa-book'

    list_display = ["name", "code"]
    list_display_links = ["name"]
    search_fields = ["name", "code"]
    fields = ["name", "code"]


class PoliceTypeAdmin(BaseAdmin):
    model_icon = 'fa fa-cab'

    list_display = ["name"]
    list_display_links = ["name"]
    search_fields = ["name"]
    fields = ["name"]


class PoliceAdmin(BaseAdmin):
    model_icon = 'fa fa-user'

    list_display = ["name", "police_code", "police_group", "imei", "police_type"]
    list_display_links = ["name"]
    list_filter = ["police_group", "police_type"]
    search_fields = ["name", "police_code"]
    fields = ["name", "police_code", "police_group", "imei", "police_type"]


xadmin.site.register(Police, PoliceAdmin)
xadmin.site.register(PoliceType, PoliceTypeAdmin)
xadmin.site.register(PoliceGroup, PoliceGroupAdmin)
