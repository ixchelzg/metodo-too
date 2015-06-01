from django.contrib import admin
from management.models import EquipoDeComputo, Tipo, Historial, Reparacion, Estado
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

action_names = {
    ADDITION: 'Addition',
    CHANGE:   'Change',
    DELETION: 'Deletion',
}
# Register your models here.

class ReparacionInline(admin.StackedInline):
    model = Reparacion
    extra = 0

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
    #que se ve en la pag del admin
    list_display = ('tipo', 'my_property','marca', 'modelo', 'estado', 'ubicacion','history_link', 'acciones')
    #list_filter = ['pub_date']
    search_fields = ['marca', 'modelo']

    def my_property(self,obj):
        return obj.user
    my_property.allow_tags = True
    my_property.short_description = "Responsable"

    def history_link(self,obj):
        return u'<a href="/management/equipodecomputo/historia%s">Ver</a>' % (obj.id)
    history_link.allow_tags = True
    history_link.short_description = "Historia"

    def acciones(self,obj):
        return u' <a href="/admin/management/equipodecomputo/%s/">Editar</a> | <a href="/admin/management/equipodecomputo/%s/delete">Eliminar</a>' % (obj.id, obj.id)
    acciones.allow_tags = True
    acciones.short_description = "Acciones"

    def get_queryset(self, request):
        qs = super(EquipoDeComputoAdmin, self).get_queryset(request)
        l = []
        for g in request.user.groups.all():
            l.append(g.name)

        if request.user.is_superuser or 'administrador' in l or 'capturista' in l :
            self.list_display_links = ['tipo']
            return qs
        self.list_display_links = None
        return qs.filter(user=request.user)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EquipoDeComputoAdmin, self).__init__(*args, **kwargs)

class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)

class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'
    def lookups(self, request, model_admin):
        return action_names.items()


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = 'user'
    parameter_name = 'user_id'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username)
            for u in User.objects.filter(pk__in =
                LogEntry.objects.values_list('user_id').distinct())
        )

class AdminFilter(UserFilter):
    """Use this filter to only show current Superusers."""
    title = 'admin'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))

class StaffFilter(UserFilter):
    """Use this filter to only show current Staff members."""
    title = 'staff'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    #readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'

#admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(EquipoDeComputo, EquipoDeComputoAdmin)

admin.site.unregister(User)

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'groups')}
        ),
    )
    list_display = ('username', 'email','grupo','acciones')

    def acciones(self,obj):
        return u' <a href="/admin/auth/user/%s/">Editar</a> | <a href="/admin/auth/user/%s/delete">Eliminar</a>' % (obj.id, obj.id)
    acciones.allow_tags = True
    acciones.short_description = "Acciones"

    def grupo(self,obj):
        gr=''
        for g in obj.groups.values_list('name',flat=True):
            gr= g
        return u'%s' % (gr)

    grupo.allow_tags = True
    grupo.short_description = "Grupo"


admin.site.register(User, MyUserAdmin)