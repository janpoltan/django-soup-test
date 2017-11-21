from django.contrib import admin
from .models import Professional, Contact

class ContactAdmin(admin.StackedInline):
    model = Contact

class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'email', 'website')
    inlines = [ContactAdmin]

admin.site.register(Professional, ProfessionalAdmin)
admin.site.register(Contact)
