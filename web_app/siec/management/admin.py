from django.contrib import admin
from management.models import EquipoDeComputo, Tipo, Historial, Reparacion, Estado

# Register your models here.

class ReparacionInline(admin.TabularInline):
    model = Reparacion
    classes = ('collapse')
    extra = 1

class EquipoDeComputoAdmin(admin.ModelAdmin):
	fieldsets = [
        (None,               {'fields': ['tipo']}),
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['marca']}),
        (None,               {'fields': ['modelo']}),
        (None,               {'fields': ['estado']}),
        (None,               {'fields': ['ubicacion']}),
    ]
	inlines = [ReparacionInline]
	#list_display = ('question_text', 'pub_date', 'was_published_recently')
	#list_filter = ['pub_date']
	search_fields = ['marca', 'modelo']

admin.site.register(EquipoDeComputo, EquipoDeComputoAdmin)
admin.site.register(Historial)
admin.site.register(Reparacion)