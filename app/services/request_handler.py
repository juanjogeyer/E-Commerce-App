import requests
import logging

def request_handler(method, url, json_data=None):
    try:
        response = requests.request(method, url, json=json_data, verify=False)
        
        # Si la respuesta es exitosa (200 o 201), procesamos la respuesta
        if response.status_code in (200, 201):
            try:
                response_data = response.json()  # Obtenemos la respuesta en formato JSON
            except ValueError:
                response_data = response.text  # En caso de que no sea JSON
            
            logging.info(f"Solicitud exitosa a {url}: {response_data}")
            return response_data
        
        # Si no se encuentra el recurso
        elif response.status_code == 404:
            logging.error(f"Recurso no encontrado en {url}")
            raise Exception(f"Recurso no encontrado en {url}")
        
        # En caso de error, solo registramos el mensaje importante
        else:
            try:
                error_data = response.json()
                mensaje_error = error_data.get("message", "Error desconocido")
                detalles_error = error_data.get("data", {})
                logging.error(f"Error en {method} a {url}: {mensaje_error}, Detalles: {detalles_error}")
                
            except ValueError:
                logging.error(f"Error en {method} a {url}: {response.status_code} - {response.text}")
            raise Exception(f"Error en la solicitud {method} a {url}: {response.status_code}")
    
    except requests.RequestException as e:
        logging.error(f"Error de conexión con {url}: {str(e)}")
        raise  # Re-lanzamos la excepción para que el código que llama a esta función pueda manejarla
    
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise  # Re-lanzamos la excepción para que se pueda manejar a un nivel superior