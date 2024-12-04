import os, requests, logging
from app.mapping import StockSchema
from app.models import Stock, Carrito
from marshmallow.exceptions import ValidationError

class ClienteInventariosService:
    
    def __init__(self):
        self.stock = Stock()
        self.URL = os.getenv('MSINVENTARIOS_URL', 'http://localhost:5004')

    def retirar_producto(self, carrito: Carrito) -> None:
        self.stock.producto = carrito.producto.id
        self.stock.cantidad = carrito.cantidad
        self.stock.entrada_salida = -1

        stock_schema = StockSchema()

        try:
            # Serializar el stock como JSON
            data = stock_schema.dump(self.stock)
            data.pop('id', None)
            r = requests.post(f'{self.URL}/inventarios/retirar', json=data, verify=False)
            response_data = r.json()  # Parsear la respuesta JSON

            if r.status_code in (200, 201):
                if 'data' in response_data:
                    try:
                        # Validar la respuesta usando el esquema actualizado
                        inventario_data = response_data['data']
                        self.stock = stock_schema.load(inventario_data)  # Validar y cargar datos en self.stock
                        logging.info(f"Stock registrado para retirada: {inventario_data}")
                    except ValidationError as e:
                        logging.error(f"Validación fallida en la respuesta: {e.messages}")
                        raise Exception(f"Validación fallida en la respuesta: {e.messages}")
                else:
                    logging.error("La respuesta no contiene el campo 'data'")
                    raise Exception("La respuesta no contiene el campo 'data'")
            else:
                logging.error(f"Error en el microservicio de inventario al retirar producto: {r.status_code} - {r.text}")
                raise Exception(f"Error en el microservicio de inventario al retirar producto: {r.status_code} - {r.text}")

        except requests.RequestException as e:
            logging.error(f"Error de conexión con el microservicio de inventario: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error al retirar producto del inventario: {str(e)}")
            raise

    
    def ingresar_producto(self) -> None:
        if not self.stock.id:
            logging.error("No se puede compensar sin un ID de transacción de retiro válido")
            raise ValueError("No se puede compensar sin un ID de transacción de retiro válido")
        
        self.stock.entrada_salida = 1
        stock_schema = StockSchema()
        
        try:
            data = stock_schema.dump(self.stock)
            r = requests.put(f'{self.URL}/inventarios/ingresar', json=data, verify=False)  # Cambiado a PUT
            
            if r.status_code == 200:
                logging.info(f"Compensación exitosa, producto devuelto a stock, id: {self.stock.id}")
            
            else:
                logging.error(f"Error al intentar compensar en el microservicio de inventario: {r.status_code} - {r.text}")
                raise Exception("Error tratando de compensar stock en el microservicio de inventario")
        
        except Exception as e:
            logging.error(f"Error al ingresar producto al inventario para compensar: {e}")
            raise