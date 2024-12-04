import os, requests, logging
from app.mapping import PagoSchema
from app.models import Pago, Producto

class ClientePagosService:
    
    def __init__(self):
        self.pago = Pago()
        self.URL = os.getenv('MSPAGOS_URL', 'http://localhost:5003')

    def registrar_pago(self, producto: Producto, medio_pago: str) -> None:
        self.pago.producto = producto.id
        self.pago.precio = producto.precio
        self.pago.medio_pago = medio_pago

        pago_schema = PagoSchema()
        pago_data = pago_schema.dump(self.pago)

        if 'id' in pago_data:
            del pago_data['id']

        try:
            r = requests.post(f'{self.URL}/pagos/add', json=pago_data, verify=False)

            if r.status_code in (200, 201):
                response_data = r.json()
                logging.info(f"Pago realizado: {response_data}")

                self.pago.id = response_data["data"].get("id")
                return response_data
            
            elif r.status_code == 404:
                logging.error("Error en el microservicio pagos: Producto no encontrado")
                raise Exception("Error en el microservicio pagos: Producto no encontrado")
            
            else:
                logging.error(f"Error inesperado en pagos: {r.status_code} - {r.text}")
                raise Exception("Error inesperado en pagos")
            
        except Exception as e:
            logging.error(f"Error al registrar el pago: {e}")
            raise
    
    def cancelar_pago(self) -> None:
        if not self.pago.id:
            logging.error("No se puede cancelar el pago sin ID")
            raise ValueError("No se puede cancelar el pago sin ID")

        try:
            r = requests.delete(f'{self.URL}/pagos/cancelar/{self.pago.id}')

            if r.status_code == 200:
                logging.info(f"Pago eliminado con éxito: id {self.pago.id}")

            else:
                logging.error(f"Error tratando de eliminar el pago: {r.status_code} - {r.text}")
                raise Exception("Error tratando de eliminar el pago")
        
        except Exception as e:
            logging.error(f"Error en la eliminación del pago: {e}")
            raise