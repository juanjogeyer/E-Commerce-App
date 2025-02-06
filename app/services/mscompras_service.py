import os
from app.mapping import CompraSchema
from app.models import Compra, Producto
from app.services.request_handler import request_handler

compra_schema = CompraSchema()

class ClienteComprasService:
    def __init__(self):
        self.compra = Compra()
        self.URL = os.getenv('MSCOMPRAS_URL', 'http://localhost:5002')
    
    def comprar(self, producto: Producto, direccion_envio: str, *args, **kwargs) -> None:
        self.compra.producto = producto.id
        self.compra.direccion_envio = direccion_envio

        data = compra_schema.dump(self.compra)
        data.pop("id", None)

        response_data = request_handler("POST", f"{self.URL}/compras", json_data=data)
        self.compra.id = response_data["data"].get("id")

    def cancelar_compra(self) -> None:
        if not self.compra.id:
            raise ValueError("No se puede cancelar una compra sin ID")
        request_handler("DELETE", f"{self.URL}/compras/{self.compra.id}")