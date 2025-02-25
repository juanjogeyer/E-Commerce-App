import os
from app import create_app

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    host = os.getenv("FLASK_HOST", "0.0.0.0")  # Usamos "0.0.0.0" como valor predeterminado
    port = int(os.getenv("FLASK_PORT", 5000))  # Usamos 5000 como valor predeterminado
    app.run(host=host, port=port)