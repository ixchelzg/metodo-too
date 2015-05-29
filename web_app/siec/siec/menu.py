"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'siec.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu
#from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class CustomMenu(Menu):
    """
    Custom Menu for siec admin site.
    """
    def init_with_context(self, context):
        #Menu.__init__(self)
        request = context['request']
        usid = request.user.id
        usuario = User.objects.get(id=usid)
        grupos = usuario.groups
        #print grupos

        if grupos == 'administrador' :
            self.children += [
                items.MenuItem(_('Dashboard'), reverse('admin:index')),
                items.MenuItem('Generar Reportes',
                    children=[
                        items.MenuItem('Tipos de equipo', '/management/reportes/tiposequipo'),
                        items.MenuItem('Equipos por responsable', '/management/reportes/porresponsable'),
                        items.MenuItem('Estado de los equipo', '/management/reportes/estadoequipos'),
                        items.MenuItem('Equipos en mantenimiento', '/management/reportes/enmantenimiento'),
                    ]
                ),
                items.AppList(
                    _('Administrar Equipos de Computo'),
                    exclude=('django.contrib.*',)
                ),
                items.AppList(
                    _('Administrar Usuarios'),
                    models=('django.contrib.*',)
                ),
                
            ]
        else:
            self.children += [
                items.MenuItem(_('Dashboard'), reverse('admin:index')),
                items.AppList(
                    _('Administrar Equipos de Computo'),
                    exclude=('django.contrib.*',)
                ),
                items.AppList(
                    _('Administrar Usuarios'),
                    models=('django.contrib.*',)
                ),
                
            ]

    # def init_with_context(self, context):
    #     """
    #     Use this method if you need to access the request context.
    #     """
    #     return super(CustomMenu, self).init_with_context(context)
