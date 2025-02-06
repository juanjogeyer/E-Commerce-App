from flask import Blueprint, request
from app.mapping import ProductoSchema, CarritoSchema, ResponseSchema
from app.services import EcommerceService
from app.services.response_message import ResponseBuilder
from app.services.exeptions import ConflictError, InternalServerError
from tenacity import retry, stop_after_attempt, wait_random

ecommerce = Blueprint('ecommerce', __name__)
response_schema = ResponseSchema()
producto_schema = ProductoSchema()
carrito_schema = CarritoSchema()

ecommerce_service = EcommerceService()

@retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(3))
@ecommerce.route('/ecommerce/comprar', methods=['POST'])
def comprar():
    response_builder = ResponseBuilder()
    carrito_schema = CarritoSchema()

    # Obtenemos el JSON del cuerpo de la solicitud
    json_data = request.get_json()

    if not json_data:
        response_builder.add_message("No se proporcionó datos").add_status_code(400)
        return response_schema.dump(response_builder.build()), 400
    
    try:
        # Deserializamos el JSON a un objeto Carrito
        carrito = carrito_schema.load(json_data)

        # Llamamos al método comprar con el objeto Carrito
        ecommerce_service.comprar(carrito)

        # Si no hubo excepciones, construye la respuesta de éxito
        data = carrito_schema.dump(carrito)
        response_builder.add_message("La compra fue exitosa").add_status_code(200).add_data(data)
        return response_schema.dump(response_builder.build()), 200

    except ConflictError as e:
        # Si hay un error de conflicto (por ejemplo, stock insuficiente), lo manejamos así
        response_builder.add_error("Compra cancelada debido a stock insuficiente. Intente con una cantidad menor o más tarde.", 409)
        return response_schema.dump(response_builder.build()), 409      # Construimos la respuesta de error

    except InternalServerError as e:
        # Si ocurre un error inesperado, lo manejammos de esta manera
        response_builder.add_error("Ocurrió un error inesperado. Intente nuevamente más tarde.", 500)
        return response_schema.dump(response_builder.build()), 500      # Construimos la respuesta de error

@retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(3))
@ecommerce.route('/ecommerce/consultar/catalogo/<int:id>', methods=['GET'])
def consultar_catalogo(id: int):
    response_builder = ResponseBuilder()
    try:
        producto = ecommerce_service.consultar_catalogo(id)
        if producto:
            data = producto_schema.dump(producto)
            response_builder.add_message("Producto encontrado").add_status_code(200).add_data(data)
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Producto NO encontrado").add_status_code(404)
            return response_schema.dump(response_builder.build()), 404
        
    except Exception as e:
        response_builder.add_message(f"Error: {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500