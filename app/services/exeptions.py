from werkzeug.exceptions import HTTPException

class ConflictError(HTTPException):
    code = 409
    description = "Conflicto en la solicitud."

    def __init__(self, description=None):
        if description:
            self.description = description
        super().__init__(description)

class InternalServerError(HTTPException):
    code = 500
    description = "Error interno del servidor."

    def __init__(self, description=None):
        if description:
            self.description = description
        super().__init__(description)
