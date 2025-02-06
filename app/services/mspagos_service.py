import os
from app.mapping import PagoSchema
from app.models import Pago, Producto
from app.services.request_handler import request_handler

class ClientePagosService:
    
    def __init__(self):
        self.pago = Pago()
        self.URL = os.getenv('MSPAGOS_URL', 'http://localhost:5003')

    def registrar_pago(self, producto: Producto, medio_pago: str) -> None:
        self.pago.producto = producto.id
        self.pago.precio = producto.precio
        self.pago.medio_pago = medio_pago

        pago_schema = PagoSchema()
        data = pago_schema.dump(self.pago)
        
        if 'id' in data:
            del data['id']

        response_data = request_handler("POST", f"{self.URL}/pagos/add", data)
        self.pago.id = response_data["data"].get("id")
    
    def cancelar_pago(self) -> None:
        if not self.pago.id:
            raise ValueError("No se puede cancelar el pago sin ID")
        request_handler("DELETE", f"{self.URL}/pagos/cancelar/{self.pago.id}")