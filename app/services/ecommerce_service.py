import logging
from app.saga import SagaBuilder, SagaError
from app.services import ClienteComprasService, ClientePagosService, ClienteInventariosService, ClienteCatalogoService
from app.models import Carrito, Producto

clienteCompras = ClienteComprasService()
clientePagos = ClientePagosService()
clienteInventario = ClienteInventariosService()
clienteCatalogo = ClienteCatalogoService()

class EcommerceService:
    """ Clase que implementa la funcionalidad de Orquestador en el patron SAGA de microservicios """
    def comprar(self, carrito: Carrito) -> None:
        
        try:
            SagaBuilder.create()\
                .action(lambda: clienteCompras.comprar(carrito.producto, carrito.direccion_envio), lambda: clienteCompras.cancelar_compra()) \
                .action(lambda: clientePagos.registrar_pago(carrito.producto, carrito.medio_pago), lambda: clientePagos.cancelar_pago()) \
                .action(lambda: clienteInventario.retirar_producto(carrito), lambda: clienteInventario.ingresar_producto()) \
                .build().execute()
        except SagaError as e:
            logging.error(e)

    def consultar_catalogo(self, id: int) -> Producto:
        result = clienteCatalogo.obtener_producto(id)
        return result