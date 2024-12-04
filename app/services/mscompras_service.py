import os, requests, logging
from urllib.parse import urljoin
from app.mapping import CompraSchema
from app.models import Compra, Producto

compra_schema = CompraSchema()

class ClienteComprasService:
    def __init__(self):
        self.compra = Compra()
        self.URL = os.getenv('MSCOMPRAS_URL', 'http://localhost:5002')
    
    def comprar(self, producto: Producto, direccion_envio: str) -> None:
        self.compra.producto = producto.id
        self.compra.direccion_envio = direccion_envio

        compra_data = compra_schema.dump(self.compra)

        # Eliminamos el campo "id" si está presente
        compra_data.pop("id", None)

        try:

            r = requests.post(f'{self.URL}/compras', json=compra_data, verify=False)

            if r.status_code in (200, 201):
                response_data = r.json()
                self.compra.id = response_data["data"].get("id")
                logging.info(f"Compra realizada: {response_data}")
                return response_data
            
            elif r.status_code == 404:
                logging.error("Error en el microservicio compras: Producto no encontrado")
                raise Exception("Error en el microservicio compras: Producto no encontrado")
            
            else:
                logging.error(f"Error inesperado en compras: {r.status_code} - {r.text}")
                raise Exception("Error inesperado en compras")
            
        except Exception as e:
            logging.error(f"Error al realizar la compra: {e}")
            raise

    def cancelar_compra(self) -> None:
        if not self.compra.id:
            logging.error("No se puede cancelar una compra sin ID")
            raise ValueError("No se puede cancelar una compra sin ID")
        
        try:
            r = requests.delete(f'{self.URL}/compras/{self.compra.id}')
            if r.status_code == 200:
                logging.info(f"Compra cancelada con éxito: id {self.compra.id}")
            else:
                logging.error(f"Error tratando de compensar la compra: {r.status_code} - {r.text}")
                raise Exception("Error tratando de compensar la compra")
        except Exception as e:
            logging.error(f"Error en la compensación de la compra: {e}")
            raise