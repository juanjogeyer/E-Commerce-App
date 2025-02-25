from marshmallow import fields, Schema, post_load
from app.models import Carrito
from marshmallow import ValidationError

class CarritoSchema(Schema):
    producto = fields.Nested("ProductoSchema")
    direccion_envio= fields.String(required=True)
    cantidad= fields.Float(required=True)
    medio_pago= fields.String(required=True)

    @post_load
    def make_carrito(self, data, **kwargs):
        # Verificamos que el producto tenga un ID
        producto = data.get("producto")
        if not producto or not hasattr(producto, "id"):
            raise ValidationError("El producto debe tener un ID válido")
        return Carrito(**data)