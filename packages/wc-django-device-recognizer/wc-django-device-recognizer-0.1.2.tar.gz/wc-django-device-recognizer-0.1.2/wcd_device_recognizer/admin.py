from django.contrib import admin

from .models import InterlocutorNetwork, Interlocutor, App, OS, Device


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = 'id', 'family', 'version',
    list_filter = 'family',
    search_fields = 'id', 'family',
    date_hierarchy = 'created_at'


@admin.register(OS)
class OSAdmin(admin.ModelAdmin):
    list_display = 'id', 'family', 'arch', 'version',
    list_filter = 'family', 'arch',
    search_fields = 'id', 'family', 'arch',
    date_hierarchy = 'created_at'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'brand', 'model', 'family', 'bitness', 'memory', 'dpr', 'viewport_width',
    )
    list_filter = 'family', 'model', 'brand', 'bitness',
    search_fields = 'id', 'family', 'model', 'brand', 'bitness',
    date_hierarchy = 'created_at'


class InterlocutorNetworkInline(admin.TabularInline):
    extra = 0
    model = InterlocutorNetwork


@admin.register(Interlocutor)
class InterlocutorAdmin(admin.ModelAdmin):
    list_display = 'id', 'os', 'device', 'app', 'outer_id',
    list_filter = 'os', 'device', 'app',
    autocomplete_fields = 'os', 'device', 'app'
    date_hierarchy = 'created_at'
    search_fields = (
        'id', 'user_agent', 'client_hints', 'outer_id',
        'device__id', 'os__id', 'app__id', 'network_connections__ip'
    )
    inlines = InterlocutorNetworkInline,

    def get_queryset(self, request):
        return super().get_queryset(request).with_relateds().distinct()
