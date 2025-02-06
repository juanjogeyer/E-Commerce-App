import os, requests, logging
from app.mapping import ProductoSchema
from urllib.parse import urljoin

producto_schema = ProductoSchema()

class ClienteCatalogoService:

    def __init__(self):
        self.URL = os.getenv('MSCATALOGO_URL', 'http://localhost:5001')

    def obtener_producto(self, id: int):

        endpoint = f'/catalogo/productos/{id}'
        url = urljoin(self.URL, endpoint)
        try:
            r = requests.get(url, verify=False)
            
            if r.status_code == 200:
                # Procesamos el JSON usando ProductoSchema
                response_data = r.json()
                producto_data = response_data.get("data", {})
                
                producto = producto_schema.load(producto_data)
                return producto
                
            elif r.status_code == 404:
                logging.warning("Producto no encontrado en el catálogo")
                return None
            
            else:
                logging.error(f"Error en la solicitud al servicio de catálogo: {r.status_code}")
                return None
            
        except Exception as e:
            logging.error(f"Error al obtener producto del catálogo: {e}")
            return None