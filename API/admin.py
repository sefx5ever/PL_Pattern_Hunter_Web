from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, SymbolHistoryData, ResearcherModel

class UserAdminConfig(UserAdmin):
    model = Account
    search_fields = ('email','user','name')
    list_filter = ('name','is_staff','is_superuser','is_active','dt_register','dt_last_updated')
    ordering = ('-dt_register',)
    list_display = ('id','email','user','name','password','is_staff','is_superuser','is_active','dt_register','dt_last_updated')
    fieldsets = (
        (None, {'fields': ('email','user','name')}),
        ('Permissions', {'fields': ('is_staff','is_superuser','is_active')}),
        ('Privacy', {'fields': ('password','hash_value')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','user','name','password','role','is_staff','is_superuser','is_active')}
        ),
    )

class SymbolHistoryDataConfig(admin.ModelAdmin):
    model = SymbolHistoryData
    search_fields = ('symbol','datetime')
    list_filter = ('symbol','datetime')
    ordering = ('-symbol','datetime')
    list_display = ('symbol','kline_size','open_price','high_price','low_price','close_price','datetime')
    fieldsets = (
        ('Paired-stock Information', {'fields': ('symbol','datetime')}),
        ('Price Details', {'fields': ('open_price','high_price','low_price','close_price')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('symbol','open_price','high_price','low_price','close_price','datetime')}
        ),
    )

class ResearcherModelConfig(admin.ModelAdmin):
    model = ResearcherModel
    search_fields = ('id_researcher','model_name')
    list_filter = ('id_researcher','model_name','dt_created')
    ordering = ('-id_researcher',)
    list_display = ('id_researcher','model_name','dt_created')
    fieldsets = (
        ('Researcher\'s Model Configuration', {'fields': ('id_researcher','model_name','dt_created')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('id_researcher','model_name')}
        ),
    )


admin.site.register(Account,UserAdminConfig)
admin.site.register(SymbolHistoryData,SymbolHistoryDataConfig)
admin.site.register(ResearcherModel,ResearcherModelConfig)