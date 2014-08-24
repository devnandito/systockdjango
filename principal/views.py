from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from principal.models import Cliente, Proveedor, Cuota, TipoProducto, TipoPago, Pedido, VencimientoCuota, Factura, Compra, Producto, DetallePedido, DetalleCompra, Ciudad, EstadoCivil
from principal.forms import FormCliente, FormCuota, FormPedido, FormProveedor, FormTipoProducto, FormTipoPago, FormVencimientoCuota, FormFactura, FormCompra, FormProducto, FormDetallePedido, FormDetalleCompra, FormCiudad, FormEstadoCivil, FormSearchVen, FormSearchCiudad, FormSearchCliente
from datetime import date, timedelta, datetime
from django.db.models import F
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/dashboard')
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			usuario = request.POST['username']
			pwd = request.POST['password']
			acceso = authenticate(username=usuario, password=pwd)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/dashboard')
				else:
					return render_to_response('noactivo.html', {'error':True, 'form':form}, context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', {'error':True, 'form':form}, context_instance=RequestContext(request))
	else:
		form = AuthenticationForm()
	return render_to_response('login.html',{'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

@login_required(login_url='/')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/')
def formcliente(request):
	usuario = request.user
	if request.method=='POST':
		form = FormCliente(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/cliente')
	else:
		form = FormCliente()
	return render_to_response('formcliente.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateCliente(request, pkcliente):
	usuario = request.user
	a=get_object_or_404(Cliente,pk=pkcliente)
	if request.method=='POST':
		form=FormCliente(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/cliente')
	else:
		form=FormCliente(instance=a)
	return render_to_response('formcliente.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewcliente(request):
	usuario = request.user
	if request.method=='POST':
		forms=FormSearchCliente(request.POST)
		if forms.is_valid():
			cliente=request.POST['cliente']
			cliente_list = Cliente.objects.filter(namecliente__icontains=cliente)
			paginator = Paginator(cliente_list,10)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				list_cli = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_cli = paginator.page(paginator.num_pages)
			return render_to_response('viewcliente.html',{'usuario':usuario, 'list_cli':list_cli,'forms':forms}, context_instance=RequestContext(request))
		else:
			cliente_list = Cliente.objects.all()
			paginator = Paginator(cliente_list,10)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				list_cli = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_cli = paginator.page(paginator.num_pages)
			return render_to_response('viewcliente.html',{'usuario':usuario, 'list_cli':list_cli,'forms':forms}, context_instance=RequestContext(request))
	else:
		forms=FormSearchCliente()
		if 'o' in request.GET:
			o=request.GET['o']
			if o == 'order':
				cliente_list=Cliente.objects.all()
			else:
				cliente_list=Cliente.objects.all().order_by(o)
		else:
			o=''
			cliente_list = Cliente.objects.all()
		paginator = Paginator(cliente_list,10)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			list_cli = paginator.page(page)
		except (EmptyPage, InvalidPage):
			list_cli = paginator.page(paginator.num_pages)
	return render_to_response('viewcliente.html', {'usuario':usuario, 'list_cli':list_cli,'forms':forms,'o':o}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formcuota(request):
	usuario = request.user
	if request.method=='POST':
		form = FormCuota(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/cuota')
	else:
		form = FormCuota()
	return render_to_response('formcuota.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateCuota(request, pkcuota):
	usuario=request.user
	a=get_object_or_404(Cuota,pk=pkcuota)
	if request.method=='POST':
		form=FormCuota(request.POST,instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/cuota')
	else:
		form=FormCuota(instance=a)
	return render_to_response('formcuota.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewcuota(request):
	usuario = request.user
	cuota_list = Cuota.objects.all()
	paginator = Paginator(cuota_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_cuota = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_cuota = paginator.page(paginator.num_pages)
	return render_to_response('viewcuota.html', {'usuario':usuario, 'list_cuota':list_cuota}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formciudad(request):
	usuario = request.user
	if request.method=='POST':
		form = FormCiudad(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/ciudad')
	else:
		form = FormCiudad()
	return render_to_response('formciudad.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateCiudad(request, pkciudad):
	usuario = request.user
	a=get_object_or_404(Ciudad,pk=pkciudad)
	if request.method=='POST':
		form=FormCiudad(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/ciudad')
	else:
		form=FormCiudad(instance=a)
	return render_to_response('formciudad.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewciudad(request):
	usuario = request.user
	if request.method=='POST':
		forms=FormSearchCiudad(request.POST)
		if forms.is_valid():
			ciudad=request.POST['ciudad']
			ciudad_list = Ciudad.objects.filter(desciudad__icontains=ciudad)
			paginator = Paginator(ciudad_list,10)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				list_ciudad = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_ciudad = paginator.page(paginator.num_pages)
			return render_to_response('viewciudad.html',{'usuario':usuario, 'list_ciudad':list_ciudad,'forms':forms}, context_instance=RequestContext(request))
		else:
			ciudad_list = Ciudad.objects.all()
			paginator = Paginator(ciudad_list,10)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				list_ciudad = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_ciudad = paginator.page(paginator.num_pages)
			return render_to_response('viewciudad.html',{'usuario':usuario, 'list_ciudad':list_ciudad,'forms':forms}, context_instance=RequestContext(request))
	else:
		forms=FormSearchCiudad()
		if 'o' in request.GET:
			o=request.GET['o']
			if o == 'order':
				ciudad_list = Ciudad.objects.all()
			else:
				ciudad_list = Ciudad.objects.all().order_by(o)
		else:
			o=''
			ciudad_list = Ciudad.objects.all()
		paginator = Paginator(ciudad_list,10)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			list_ciudad = paginator.page(page)
		except (EmptyPage, InvalidPage):
			list_ciudad = paginator.page(paginator.num_pages)
	return render_to_response('viewciudad.html',{'usuario':usuario, 'list_ciudad':list_ciudad,'forms':forms,'o':o}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formestadocivil(request):
	usuario = request.user
	if request.method=='POST':
		form = FormEstadoCivil(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/estadocivil')
	else:
		form = FormEstadoCivil()
	return render_to_response('formestadocivil.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateEstadoCivil(request, pkestadocivil):
	usuario = request.user
	a=get_object_or_404(EstadoCivil,pk=pkestadocivil)
	if request.method=='POST':
		form=FormEstadoCivil(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/estadocivil')
	else:
		form=FormEstadoCivil(instance=a)
	return render_to_response('formestadocivil.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewestadocivil(request):
	usuario = request.user
	estadocivil_list = EstadoCivil.objects.all()
	paginator = Paginator(estadocivil_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_estadocivil = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_estadocivil = paginator.page(paginator.num_pages)
	return render_to_response('viewestadocivil.html',{'usuario':usuario, 'list_estadocivil':list_estadocivil}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formproveedor(request):
	usuario = request.user
	if request.method=='POST':
		form = FormProveedor(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/proveedor')
	else:
		form = FormProveedor()
	return render_to_response('formproveedor.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateProveedor(request, pkproveedor):
	usuario = request.user
	a=get_object_or_404(Proveedor,pk=pkproveedor)
	if request.method=='POST':
		form=FormProveedor(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/proveedor')
	else:
		form=FormProveedor(instance=a)
	return render_to_response('formproveedor.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewproveedor(request):
	usuario = request.user
	proveedor_list = Proveedor.objects.all()
	paginator = Paginator(proveedor_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_proveedor = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_proveedor = paginator.page(paginator.num_pages)
	return render_to_response('viewproveedor.html', {'usuario':usuario, 'list_proveedor':list_proveedor}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formtipoproducto(request):
	usuario = request.user
	if request.method=='POST':
		form = FormTipoProducto(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/tipoproducto')
	else:
		form = FormTipoProducto()
	return render_to_response('formtipoproducto.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateTipoProducto(request, pktipoproducto):
	usuario = request.user
	a=get_object_or_404(TipoProducto,pk=pktipoproducto)
	if request.method=='POST':
		form=FormTipoProducto(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/tipoproducto')
	else:
		form=FormTipoProducto(instance=a)
	return render_to_response('formtipoproducto.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewtipoproducto(request):
	usuario = request.user
	tipoprod_list = TipoProducto.objects.all()
	paginator = Paginator(tipoprod_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_tipoprod = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_tipoprod = paginator.page(paginator.num_pages)
	return render_to_response('viewtipoproducto.html', {'usuario':usuario, 'list_tipoprod':list_tipoprod}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formtipopago(request):
	usuario = request.user
	if request.method=='POST':
		form = FormTipoPago(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/tipopago')
	else:
		form = FormTipoPago()
	return render_to_response('formtipopago.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateTipoPago(request, pktipopago):
	usuario = request.user
	a=get_object_or_404(TipoPago,pk=pktipopago)
	if request.method=='POST':
		form=FormTipoPago(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/tipopago')
	else:
		form=FormTipoPago(instance=a)
	return render_to_response('formtipopago.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewtipopago(request):
	usuario = request.user
	tipopago_list = TipoPago.objects.all()
	paginator = Paginator(tipopago_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_tipopago = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_tipopago = paginator.page(paginator.num_pages)
	return render_to_response('viewtipopago.html', {'usuario':usuario, 'list_tipopago':list_tipopago}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formpedido(request):
	usuario = request.user
	if request.method=='POST':
		form = FormPedido(request.POST)
		if form.is_valid():
			form.save()
			ncuotas=int(request.POST['fkcuota'])
			pedidos=Pedido.objects.all()
			longp=len(pedidos)
			fkpedido1=pedidos[longp-1].id
			dias=0
			for i in range(1,ncuotas+1):
				if i == 1:
					formv=VencimientoCuota(nrocuota=i,fechaven=date.today(),fkpedido_id=fkpedido1)
					formv.save()
				else:
					formv=VencimientoCuota(nrocuota=i,fechaven=date.today()+timedelta(days=dias),fkpedido_id=fkpedido1)
					formv.save()
				dias=dias+30
			return HttpResponseRedirect('/view/pedido')
	else:
		form = FormPedido()
	return render_to_response('formpedido.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updatePedido(request, pkpedido):
	usuario = request.user
	a=get_object_or_404(Pedido,pk=pkpedido)
	if request.method=='POST':
		form=FormPedido(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/pedido')
	else:
		form=FormPedido(instance=a)
	return render_to_response('formpedido.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewpedido(request):
	usuario = request.user
	pedido_list = Pedido.objects.all()
	paginator = Paginator(pedido_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_pedido = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_pedido = paginator.page(paginator.num_pages)
	return render_to_response('viewpedido.html', {'usuario':usuario, 'list_pedido':list_pedido}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formvencimientocuota(request):
	usuario = request.user
	if request.method=='POST':
		form = FormVencimientoCuota(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/vencimiento')
	else:
		form = FormVencimientoCuota()
	return render_to_response('formvencimiento.html',{'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateVencimientoCuota(request, pkvencimiento):
	usuario = request.user
	a=get_object_or_404(VencimientoCuota,pk=pkvencimiento)
	if request.method=='POST':
		form=FormVencimientoCuota(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/vencimiento')
	else:
		form=FormVencimientoCuota(instance=a)
	return render_to_response('formvencimiento.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewvencimientocuota(request):
	usuario = request.user
	venc_list = VencimientoCuota.objects.all()
	paginator = Paginator(venc_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_venc = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_venc = paginator.page(paginator.num_pages)
	return render_to_response('viewvencimiento.html', {'usuario':usuario, 'list_venc':list_venc}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formfactura(request):
	usuario = request.user
	if request.method=='POST':
		form = FormFactura(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/factura')
	else:
		form = FormFactura()
	return render_to_response('formfactura.html', {'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateFactura(request, pkfactura):
	usuario = request.user
	a=get_object_or_404(Factura,pk=pkfactura)
	if request.method=='POST':
		form=FormFactura(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/factura')
	else:
		form=FormFactura(instance=a)
	return render_to_response('formfactura.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewfactura(request):
	usuario = request.user
	factura_list= Factura.objects.all()
	paginator = Paginator(factura_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_factura = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_factura = paginator.page(paginator.num_pages)
	return render_to_response('viewfactura.html', {'usuario':usuario, 'list_factura':list_factura}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formcompra(request):
	usuario = request.user
	if request.method=='POST':
		form = FormCompra(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/compra')
	else:
		form = FormCompra()
	return render_to_response('formcompra.html', {'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateCompra(request, pkcompra):
	usuario = request.user
	a=get_object_or_404(Factura,pk=pkcompra)
	if request.method=='POST':
		form=FormCompra(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/compra')
	else:
		form=FormCompra(instance=a)
	return render_to_response('formcompra.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewcompra(request):
	usuario = request.user
	compra_list = Compra.objects.all()
	paginator = Paginator(compra_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_compra = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_compra = paginator.page(paginator.num_pages)
	return render_to_response('viewcompra.html', {'usuario':usuario, 'list_compra':list_compra}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formproducto(request):
	usuario = request.user
	if request.method=='POST':
		form = FormProducto(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/producto')
	else:
		form = FormProducto()
	return render_to_response('formproducto.html', {'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateProducto(request, pkproducto):
	usuario = request.user
	a=get_object_or_404(Producto,pk=pkproducto)
	if request.method=='POST':
		form=FormProducto(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/producto')
	else:
		form=FormProducto(instance=a)
	return render_to_response('formproducto.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewproducto(request):
	usuario = request.user
	producto_list = Producto.objects.all()
	paginator = Paginator(producto_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_producto = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_producto = paginator.page(paginator.num_pages)
	return render_to_response('viewproducto.html', {'usuario':usuario, 'list_producto':list_producto}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formdetallepedido(request):
	usuario = request.user
	if request.method=='POST':
		form = FormDetallePedido(request.POST)
		if form.is_valid():
			form.save()
			cant=request.POST['cantidad']
			fkprod=request.POST['fkproducto']
			prod=Producto.objects.get(pk=fkprod)
			prod.stock=F('stock')-cant
			prod.save()
			return HttpResponseRedirect('/view/detallepedido')
	else:
		form = FormDetallePedido()
	return render_to_response('formdetallepedido.html', {'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateDetallePedido(request, pkdetallepedido):
	usuario = request.user
	a=get_object_or_404(DetallePedido,pk=pkdetallepedido)
	if request.method=='POST':
		form=FormDetallePedido(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/detallepedido')
	else:
		form=FormDetallePedido(instance=a)
	return render_to_response('formdetallepedido.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewdetallepedido(request):
	usuario = request.user
	detallepedido_list=DetallePedido.objects.all().order_by('fkpedido')
	paginator = Paginator(detallepedido_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_detallepedido = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_detallepedido = paginator.page(paginator.num_pages)
	return render_to_response('viewdetallepedido.html', {'usuario':usuario, 'list_detallepedido':list_detallepedido}, context_instance=RequestContext(request))

@login_required(login_url='/')
def formdetallecompra(request):
	usuario = request.user
	if request.method=='POST':
		form = FormDetalleCompra(request.POST)
		if form.is_valid():
			form.save()
			cant=request.POST['cantidadcompra']
			fkprod=request.POST['fkproducto']
			prod=Producto.objects.get(pk=fkprod)
			prod.stock=F('stock')+cant
			prod.save()
			return HttpResponseRedirect('/view/detallecompra')
	else:
		form = FormDetalleCompra()
	return render_to_response('formdetallecompra.html', {'usuario':usuario, 'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def updateDetalleCompra(request, pkdetallecompra):
	usuario = request.user
	a=get_object_or_404(DetalleCompra,pk=pkdetallecompra)
	if request.method=='POST':
		form=FormDetalleCompra(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/view/detallecompra')
	else:
		form=FormDetalleCompra(instance=a)
	return render_to_response('formdetallecompra.html',{'usuario':usuario,'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewdetallecompra(request):
	usuario = request.user
	detallecompra_list = DetalleCompra.objects.all()
	paginator = Paginator(detallecompra_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_detallecompra = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_detallecompra = paginator.page(paginator.num_pages)
	return render_to_response('viewdetallecompra.html', {'usuario':usuario, 'list_detallecompra':list_detallecompra}, context_instance=RequestContext(request))

@login_required(login_url='/')
def searchven(request):
	usuario=request.user
	if request.method=='POST':
		forms=FormSearchVen(request.POST)
		if forms.is_valid():
			fecha=request.POST['fecha']
			venc_list=VencimientoCuota.objects.filter(fechaven=fecha)
			paginator = Paginator(venc_list,10)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				list_venc = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_venc = paginator.page(paginator.num_pages)
			return render_to_response('searchven.html',{'usuario':usuario, 'list_venc':list_venc,'forms':forms}, context_instance=RequestContext(request))
		else:
			venc_list = VencimientoCuota.objects.all()
			paginator = Paginator(venc_list,10)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				list_venc = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_venc = paginator.page(paginator.num_pages)
			return render_to_response('searchven.html',{'usuario':usuario, 'list_venc':list_venc,'forms':forms}, context_instance=RequestContext(request))
	else:
		dateToday=date.today()
		forms=FormSearchVen()
		if 'o' in request.GET:
			o=request.GET['o']
			if o == 'order':
				venc_list = VencimientoCuota.objects.all()
			else:
				venc_list = VencimientoCuota.objects.all().order_by(o)
		else:
			o=''
			venc_list = VencimientoCuota.objects.all()
		paginator = Paginator(venc_list,10)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			list_venc = paginator.page(page)
		except (EmptyPage, InvalidPage):
			list_venc = paginator.page(paginator.num_pages)
	return render_to_response('searchven.html',{'usuario':usuario, 'list_venc':list_venc, 'forms':forms,'dateToday':dateToday,'o':o}, context_instance=RequestContext(request))

@login_required(login_url='/')
def viewtest(request):
	usuario=request.user
	list_det=DetallePedido.objects.all().select_related('fkpedido').order_by('fkpedido')
	paginator = Paginator(list_det,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		detalle_list = paginator.page(page)
	except (EmptyPage, InvalidPage):
		detalle_list = paginator.page(paginator.num_pages)
	return render_to_response('test.html',{'usuario':usuario,'detalle_list':detalle_list}, context_instance=RequestContext(request))

@login_required(login_url='/')
def addDetPedido(request, fkpedido):
	if request.method=='POST':
		a=DetallePedido(fkpedido_id=request.POST['pedido'],fkproducto_id=request.POST['producto'],cantidad=request.POST['cant'])
		a.save()
		return HttpResponseRedirect('/test')
		# fkp=request.POST['pedido']
		# prod=request.POST['producto']
		# cant=request.POST['cant']
		# return render_to_response('test2.html',{'fkp':fkp,'prod':prod,'cant':cant}, context_instance=RequestContext(request))
	pedido=fkpedido
	fkproducto=Producto.objects.all()
	return render_to_response('test1.html',{'pedido':pedido,'fkproducto':fkproducto}, context_instance=RequestContext(request))

@login_required(login_url='/')
def paginationTest(request):
	usuario = request.user
	if 'o' in request.GET:
		o=request.GET['o']
		if o == 'order':
			venc_list = VencimientoCuota.objects.all()
		else:
			venc_list = VencimientoCuota.objects.all().order_by(o)
	else:
		o=''
		venc_list = VencimientoCuota.objects.all()
	paginator = Paginator(venc_list,10)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		list_venc = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_venc = paginator.page(paginator.num_pages)
	return render_to_response('test2.html', {'usuario':usuario, 'list_venc':list_venc,'o':o}, context_instance=RequestContext(request))