from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from management.models import EquipoDeComputo, Reparacion, Tipo
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


# from admin_tools.menu import Menu

# class MyMenu(Menu):
#     class Media:
#         css = ('/media/css/mymenu.css',)
#         js = ('/media/js/mymenu.js',)

def index(request):
    return HttpResponse("Hello, world. You're at the SIEC management index.")

def piecharts(request):
	#instantiate a drawing object
	import piechart
	d = piechart.BreakdownPieDrawing()

	#get a GIF (or PNG, JPG, or whatever)
	binaryStuff = d.asString('gif')
	return HttpResponse(binaryStuff, 'image/gif')
	#return render_to_response('management/pieChart.html', {'lachart': binaryStuff, 'hola': 'popo'})

def tiposequipo(request):
	equipos = EquipoDeComputo.objects.order_by('tipo')

	return render(request,'management/pieChartTipos.html', {'lachart': reverse('piecharts'), 'equipos':equipos , 'titulo': 'Tipos de equipo'})
	#return render(request, "subscription/monitorSizes.html", {'form':form,'message':'','graph':reverse('show_image')})


def piechartresponsable(request):
	#instantiate a drawing object
	import piechartporresponsable
	d = piechartporresponsable.BreakdownPieDrawing()

	#get a GIF (or PNG, JPG, or whatever)
	binaryStuff = d.asString('gif')
	return HttpResponse(binaryStuff, 'image/gif')
	#return render_to_response('management/pieChart.html', {'lachart': binaryStuff, 'hola': 'popo'})

def porresponsable(request):
	return render(request,'management/pieChartPorResponsable.html', {'lachart': reverse('piechartresponsable'), 'titulo': 'Equipos por responsable'})
	#return render(request, "subscription/monitorSizes.html", {'form':form,'message':'','graph':reverse('show_image')})


def piechartporestado(request):
	#instantiate a drawing object
	import piechartestado
	d = piechartestado.BreakdownPieDrawing()

	#get a GIF (or PNG, JPG, or whatever)
	binaryStuff = d.asString('gif')
	return HttpResponse(binaryStuff, 'image/gif')
	#return render_to_response('management/pieChart.html', {'lachart': binaryStuff, 'hola': 'popo'})

def porestado(request):
	return render(request,'management/pieChartPorEstado.html', {'lachart': reverse('piechartporestado'), 'titulo': 'Estado de los equipos'})
	#return render(request, "subscription/monitorSizes.html", {'form':form,'message':'','graph':reverse('show_image')})


def enmantenimiento(request):
	equipos = EquipoDeComputo.objects.filter(estado=5)
	for es in equipos:
		rep = Reparacion.objects.filter(equipodecomputo=es.id).latest('fecha')
		es.rep = rep
	return render(request,'management/EnMantenimiento.html', {'equipos': equipos, 'titulo': 'Equipos en mantenimiento'})
	#return render(request, "subscription/monitorSizes.html", {'form':form,'message':'','graph':reverse('show_image')})

def historia(request, eqid=None):
	equipos = EquipoDeComputo.objects.get(id=eqid)
	reparaciones = Reparacion.objects.filter(equipodecomputo=eqid)

	action_list = LogEntry.objects.filter(
		content_type_id = ContentType.objects.get_for_model(EquipoDeComputo).id,
		object_id = equipos.id,
	)

	return render(request,'management/historia.html', {'equipos': equipos, 'reparaciones': reparaciones, 'action_list' : action_list, 'titulo': 'Historia'})