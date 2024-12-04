class SagaError(Exception):
    """Excepción personalizada para manejar errores en la ejecución de la saga."""
    def __init__(self, message):
        super().__init__(message)