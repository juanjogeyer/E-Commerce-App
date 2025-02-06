import logging
from saga import SagaBuilder, SagaError
from app.services import ClienteComprasService, ClientePagosService, ClienteInventariosService, ClienteCatalogoService
from app.services.exeptions import ConflictError, InternalServerError
from app.models import Carrito, Producto

clienteCompras = ClienteComprasService()
clientePagos = ClientePagosService()
clienteInventario = ClienteInventariosService()
clienteCatalogo = ClienteCatalogoService()

class EcommerceService:
    """ Clase que implementa la funcionalidad de Orquestador en el patrón SAGA de microservicios """
    
    def comprar(self, carrito: Carrito) -> None:
        stock_retirado = False
        
        try:
            SagaBuilder.create()\
                .action(lambda *_: clienteCompras.comprar(carrito.producto, carrito.direccion_envio), 
                        lambda *_: clienteCompras.cancelar_compra()) \
                .action(lambda *_: clientePagos.registrar_pago(carrito.producto, carrito.medio_pago), 
                        lambda *_: clientePagos.cancelar_pago()) \
                .action(lambda *_: self.retirar_stock(carrito, stock_retirado), 
                        lambda *_: self.ingresar_stock_si_fue_retirado(stock_retirado)) \
                .build().execute()
                
        except SagaError as e:
            logging.error(f"SAGA ERROR: {e}")
            if "409" in str(e):
                logging.error(f"Conflicto de stock: {e}")
                raise ConflictError(f"Compra cancelada debido a stock insuficiente: {e}")  # ← HTTP 409
            logging.error(f"Error inesperado en SAGA: {e}")
            raise InternalServerError(f"Error inesperado: {e}")  # ← HTTP 500

    def retirar_stock(self, carrito: Carrito, stock_retirado: bool):
        """ Intenta retirar stock y marca si fue exitoso. """
        try:
            clienteInventario.retirar_producto(carrito)
            stock_retirado = True 
        except ConflictError as e:
            logging.error(f"No se pudo retirar stock: {e}")
            raise e

    def ingresar_stock_si_fue_retirado(self, stock_retirado: bool):
        """ Solo ingresa stock si efectivamente se retiró previamente. """
        if stock_retirado:
            clienteInventario.ingresar_producto()

    def consultar_catalogo(self, id: int) -> Producto:
        result = clienteCatalogo.obtener_producto(id)
        return result