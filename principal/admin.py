from django.contrib import admin
from principal.models import Cliente, Proveedor, Cuota, TipoProducto, TipoPago, Pedido, VencimientoCuota, Factura, Compra, Producto, DetallePedido, DetalleCompra, Ciudad, EstadoCivil

class AdminCliente(admin.ModelAdmin):
	list_display = ('namecliente','lastnamecliente','dircliente','phonecliente')

class AdminCiudad(admin.ModelAdmin):
	list_display = ('id','desciudad',)

class AdminCompra(admin.ModelAdmin):
	list_display = ('nrofactura', 'fechacompra','fkuser','fkproveedor')

class AdminCuota(admin.ModelAdmin):
	list_display = ('id','cantcuota')

class AdminDetalleCompra(admin.ModelAdmin):
	list_display = ('fkproducto','fkcompra','cantidadcompra')

class AdminDetallePedido(admin.ModelAdmin):
	list_display = ('fkpedido','fkproducto','cantidad')

class AdminEstadoCivil(admin.ModelAdmin):
	list_display = ('id', 'desestadocivil',)

class AdminFactura(admin.ModelAdmin):
	list_display = ('dkpedido','fechafactura')

class AdminPedido(admin.ModelAdmin):
	list_display = ('fechapedido','fkcliente','fktipopago','fkcuota')

class AdminProducto(admin.ModelAdmin):
	list_display = ('desprod','stock','fktipoprod')

class AdminProveedor(admin.ModelAdmin):
	list_display = ('nameprov','dirprov','telprov','celprov')

class AdminTipoProducto(admin.ModelAdmin):
	list_display = ('id','destipoprod')

class AdminTipoPago(admin.ModelAdmin):
	list_display = ('id','destipopago')

class AdminVencimientoCuota(admin.ModelAdmin):
	list_display = ('nrocuota','fechaven','fkpedido')

admin.site.register(Cliente, AdminCliente)
admin.site.register(Ciudad, AdminCiudad)
admin.site.register(Compra, AdminCompra)
admin.site.register(Cuota, AdminCuota)
admin.site.register(DetalleCompra, AdminDetalleCompra)
admin.site.register(EstadoCivil, AdminEstadoCivil)
admin.site.register(Pedido, AdminPedido)
admin.site.register(DetallePedido, AdminDetallePedido)
admin.site.register(Producto, AdminProducto)
admin.site.register(Proveedor, AdminProveedor)
admin.site.register(TipoPago, AdminTipoPago)
admin.site.register(TipoProducto, AdminTipoProducto)
admin.site.register(VencimientoCuota, AdminVencimientoCuota)