from django.forms import ModelForm
from django import forms
from principal.models import Cliente, Proveedor, Cuota, TipoProducto, TipoPago, Pedido, VencimientoCuota, Factura, Compra, Producto, DetallePedido, DetalleCompra, Ciudad, EstadoCivil

class FormCliente(ModelForm):
	class Meta:
		model = Cliente

class FormCiudad(ModelForm):
	class Meta:
		model = Ciudad

class FormEstadoCivil(ModelForm):
	class Meta:
		model = EstadoCivil

class FormProveedor(ModelForm):
	class Meta:
		model = Proveedor

class FormCuota(ModelForm):
	class Meta:
		model = Cuota

class FormTipoProducto(ModelForm):
	class Meta:
		model = TipoProducto

class FormTipoPago(ModelForm):
	class Meta:
		model = TipoPago

class FormPedido(ModelForm):
	class Meta:
		model = Pedido

class FormVencimientoCuota(ModelForm):
	class Meta:
		model = VencimientoCuota

class FormFactura(ModelForm):
	class Meta:
		model = Factura

class FormCompra(ModelForm):
	class Meta:
		model = Compra

class FormProducto(ModelForm):
	class Meta:
		model = Producto
		exclude = ['detalles']

class FormDetallePedido(ModelForm):
	class Meta:
		model = DetallePedido

class FormDetalleCompra(ModelForm):
	class Meta:
		model = DetalleCompra

class FormSearchVen(forms.Form):
	fecha = forms.DateField(label='Fecha', error_messages={'required':'Debe ingresar una fecha'})

class FormSearchCiudad(forms.Form):
	ciudad = forms.CharField(label='Ciudad', error_messages={'required':'Debe ingresar una ciudad'})

class FormSearchCliente(forms.Form):
	cliente = forms.CharField(label='Cliente', error_messages={'required': 'Debe ingresar un nombre de cliente'})