from django.db import models
from django.contrib.auth.models import User

class EstadoCivil(models.Model):
	desestadocivil = models.CharField(blank=False, max_length=140)
	class Meta:
		verbose_name = 'Estado Civil'
		verbose_name_plural = 'Estados Civiles'
	def __unicode__(self):
		return "%s" %(self.desestadocivil)

class Ciudad(models.Model):
	desciudad = models.CharField(blank=False, max_length=140)
	class Meta:
		verbose_name = 'Ciudad'
		verbose_name_plural = 'Ciudades'
	def __unicode__(self):
		return "%s" %(self.desciudad)

class Cliente(models.Model):
	namecliente = models.CharField(blank=False, max_length=140)
	lastnamecliente = models.CharField(blank=False, max_length=140)
	fechanac = models.CharField(blank=False, max_length=140)
	cedula = models.CharField(blank=False, max_length=10)
	fkestadocivil = models.ForeignKey(EstadoCivil)
	dircliente = models.CharField(blank=False, max_length=140)
	fkciudad = models.ForeignKey(Ciudad)
	barrio = models.CharField(blank=False, max_length=140)
	profesion = models.CharField(blank=False, max_length=140)
	phonecliente = models.CharField(blank=False, max_length=15)
	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clientes'
	def __unicode__(self):
		return "%s %s" %(self.namecliente,self.lastnamecliente)

class Proveedor(models.Model):
    nameprov = models.CharField(blank=False, max_length=140)
    dirprov = models.CharField(blank=False, max_length=140)
    telprov = models.CharField(blank=False, max_length=15)
    celprov = models.CharField(blank=True, max_length=10)
    class Meta:
    	verbose_name = 'Proveedor'
    	verbose_name_plural = 'Proveedores'
    def __unicode__(self):
    	return '%s' %(self.nameprov)

class Cuota(models.Model):
	cantcuota = models.IntegerField(blank=False)
	class Meta:
		verbose_name = 'Cuota'
		verbose_name_plural = 'Cuotas'
	def __unicode__(self):
		return "%s" %(self.cantcuota)

class TipoProducto(models.Model):
	destipoprod = models.CharField(blank=False, max_length=140)
	class Meta:
		verbose_name = 'Tipo Producto'
		verbose_name_plural = 'Tipos Productos'
	def __unicode__(self):
		return "%s" %(self.destipoprod)

class TipoPago(models.Model):
	destipopago = models.CharField(blank=False, max_length=140)
	class Meta:
		verbose_name = 'Tipo Pago'
		verbose_name_plural = 'Tipos Pagos'
	def __unicode__(self):
		return "%s" %(self.destipopago)

class Pedido(models.Model):
	fechapedido = models.DateField(auto_now=True)
	fkcliente = models.ForeignKey(Cliente)
	fktipopago = models.ForeignKey(TipoPago)
	fkcuota = models.ForeignKey(Cuota)
	class Meta:
		verbose_name = 'Pedido'
		verbose_name_plural = 'Pedidos'
	def __unicode__(self):
		return "%s" %(self.id)

class VencimientoCuota(models.Model):
	nrocuota = models.IntegerField(blank=False)
	fechaven = models.DateField(blank=False) #no tiene que ser auto
	fkpedido = models.ForeignKey(Pedido)
	class Meta:
		verbose_name = 'Vencimiento Cuota'
		verbose_name_plural = 'Vencimientos Cuotas'
	def __unicode__(self):
		return "%s" %(self.nrocuota)

class Factura(models.Model):
	fkpedido = models.ForeignKey(Pedido)
	fechafactura = models.DateField(auto_now=True)
	class Meta:
		verbose_name = 'Factura'
		verbose_name_plural = 'Facturas'
	def __unicode__(sefl):
		return "%s" %(self.fechafactura)

class Compra(models.Model):
	nrofactura = models.IntegerField(blank=False)
	fechacompra = models.DateField(auto_now=True)
	fkuser = models.ForeignKey(User)
	fkproveedor = models.ForeignKey(Proveedor)
	class Meta:
		verbose_name = 'Compra'
		verbose_name_plural = 'Compras'
	def __unicode__(self):
		return "%s" %(self.nrofactura)

class Producto(models.Model):
	desprod = models.CharField(blank=False, max_length=140)
	stock = models.IntegerField(blank=False, default='0')
	fktipoprod = models.ForeignKey(TipoProducto)
	detalles = models.ManyToManyField(Compra, through='DetalleCompra')
	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
	def __unicode__(self):
		return "%s %s" %(self.desprod, self.fktipoprod)

class DetallePedido(models.Model):
	fkpedido = models.ForeignKey(Pedido)
	fkproducto = models.ForeignKey(Producto)
	cantidad = models.IntegerField(blank=False)
	class Meta:
		verbose_name = 'Detalle Pedido'
		verbose_name_plural = 'Detalles Pedidos'
	def __unicode__(self):
		return "%s" %(self.cantidad)

class DetalleCompra(models.Model):
	fkproducto = models.ForeignKey(Producto)
	fkcompra = models.ForeignKey(Compra)
	cantidadcompra = models.IntegerField(blank=False, default='0')
	class Meta:
		verbose_name = 'Detalle Compra'
		verbose_name_plural = 'Destalles Compras'
	def __unicode__(self):
		return "%s" %(self.fkproducto)