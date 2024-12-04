from dataclasses import dataclass
from app.models import Producto

@dataclass
class Carrito:
    producto: Producto
    direccion_envio: str
    cantidad: float
    medio_pago: str