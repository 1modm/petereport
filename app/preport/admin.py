from django.contrib import admin
from .models import DB_Finding, DB_Customer, DB_Product, DB_Report
# Register your models here.

admin.site.register([
    DB_Customer,
    DB_Product,
    DB_Report
])

@admin.register(DB_Finding)
class DB_FindingAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
