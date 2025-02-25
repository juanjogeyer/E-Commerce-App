import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from app import create_app  # Asegúrate de importar tu aplicación Flask
from app.services import EcommerceService
from app.models import Carrito, Producto
from app.services.exeptions import ConflictError, InternalServerError

class TestEcommerce(unittest.TestCase):

    def setUp(self):
        """Configuramos la aplicación Flask para las pruebas."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('app.services.EcommerceService.comprar')
    def test_comprar_exitoso(self, mock_comprar):
        """Prueba que la compra se realiza correctamente."""
        # Configuramos el mock para simular una compra exitosa
        mock_comprar.return_value = None

        # Datos de la compra
        payload = {
            "producto": {
                "id": 1,
                "nombre": "Mouse",
                "precio": 30,
                "activado": True
            },
            "direccion_envio": "San Martin 789",
            "cantidad": 1,
            "medio_pago": "Efectivo"
        }

        # Realiza la solicitud POST
        response = self.client.post('/ecommerce/comprar', json=payload)

        # Verifica la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "La compra fue exitosa")

    @patch('app.services.EcommerceService.comprar')
    def test_comprar_error_stock(self, mock_comprar):
        """Prueba que se maneja correctamente un error de stock insuficiente."""
        # Configuramos el mock para simular un error de stock
        mock_comprar.side_effect = ConflictError("Stock insuficiente")

        # Datos de la compra
        payload = {
            "producto": {
                "id": 1,
                "nombre": "Mouse",
                "precio": 30,
                "activado": True
            },
            "direccion_envio": "San Martin 789",
            "cantidad": 1,
            "medio_pago": "Efectivo"
        }

        # Realiza la solicitud POST
        response = self.client.post('/ecommerce/comprar', json=payload)

        # Verifica la respuesta
        self.assertEqual(response.status_code, 409)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Compra cancelada debido a stock insuficiente. Intente con una cantidad menor o más tarde.")

    @patch('app.services.EcommerceService.comprar')
    def test_comprar_error_interno(self, mock_comprar):
        """Prueba que se maneja correctamente un error interno del servidor."""
        # Configuramos el mock para simular un error interno
        mock_comprar.side_effect = InternalServerError("Error inesperado")

        # Datos de la compra
        payload = {
            "producto": {
                "id": 1,
                "nombre": "Mouse",
                "precio": 30,
                "activado": True
            },
            "direccion_envio": "San Martin 789",
            "cantidad": 1,
            "medio_pago": "Efectivo"
        }

        # Realiza la solicitud POST
        response = self.client.post('/ecommerce/comprar', json=payload)

        # Verifica la respuesta
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Ocurrió un error inesperado. Intente nuevamente más tarde.")

if __name__ == '__main__':
    unittest.main()