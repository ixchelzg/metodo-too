from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
	# ex: /management/
    url(r'^$', views.index, name='index'),
	# ex: /management/charts/bar/
	url(r'^charts/tiposequipo/$', views.piecharts, name='piecharts'),
	url(r'^reportes/tiposequipo/$', views.tiposequipo, name='tiposequipo'),
	
	url(r'^charts/porresponsable/$', views.piechartresponsable, name='piechartresponsable'),
	url(r'^reportes/porresponsable/$', views.porresponsable, name='porresponsable'),

	url(r'^charts/estadoequipos/$', views.piechartporestado, name='piechartporestado'),
	url(r'^reportes/estadoequipos/$', views.porestado, name='porestado'),

	url(r'^reportes/enmantenimiento/$', views.enmantenimiento, name='enmantenimiento'),
	url(r'^equipodecomputo/historia(?P<eqid>[0-9]+)/$', views.historia),

]
