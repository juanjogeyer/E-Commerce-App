import os
from app.mapping import StockSchema
from app.models import Stock, Carrito
from app.services.request_handler import request_handler
import json

class ClienteInventariosService:
    
    def __init__(self):
        self.stock = Stock()
        self.URL = os.getenv('MSINVENTARIOS_URL', 'http://inventarios.ecommerce.local:5000')

    def retirar_producto(self, carrito: Carrito) -> None:
        self.stock.producto = carrito.producto.id
        self.stock.cantidad = carrito.cantidad
        self.stock.entrada_salida = -1

        stock_schema = StockSchema()
        data = stock_schema.dump(self.stock)
        data.pop('id', None)
        try:
            response_data = request_handler("POST", f"{self.URL}/inventarios/retirar", data)

            if 'data' in response_data:
                self.stock = stock_schema.load(response_data['data'])
        except Exception as e:
            raise Exception(f"Error en retirar_producto: {str(e)}")

    def ingresar_producto(self) -> None:
        if not self.stock.id:
            raise ValueError("No se puede compensar sin un ID de transacción de retiro válido")
        
        self.stock.entrada_salida = 1
        stock_schema = StockSchema()
        data = stock_schema.dump(self.stock)
        request_handler("PUT", f"{self.URL}/inventarios/ingresar", data)