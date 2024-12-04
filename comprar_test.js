import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check, sleep } from 'k6';

// Métrica personalizada para rastrear el estado de las respuestas
const statusTrend = new Trend('status_codes');

export const options = {
    stages: [
        { duration: '15s', target: 60 }, // Escalar hasta 100 usuarios simultáneos en 15 segundos
        { duration: '30s', target: 60 }, // Mantener 100 usuarios simultáneos durante 30 segundos
        { duration: '15s', target: 0 },  // Reducir a 0 usuarios simultáneos en 15 segundos
    ],
};

export default function () {
    const BASE_URL = 'http://localhost:5000/ecommerce/comprar'; // URL del servidor de desarrollo

    // Datos de ejemplo para simular una compra
    const payload = JSON.stringify({
        producto: {
            id: 2,
            nombre: "Laptop HP",
            precio: 750,
            activado: true
        },
        direccion_envio: "Libertador 124",
        cantidad: 1,
        medio_pago: "Efectivo",
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Realizar la solicitud POST al endpoint de compra
    const res = http.post(BASE_URL, payload, params);

    // Registrar métricas de los estados HTTP
    statusTrend.add(res.status);

    // Validaciones básicas
    check(res, {
        'status is 200': (r) => r.status === 200,
        'status is 400': (r) => r.status === 400,
    });

    sleep(1); // Simular espera de 1 segundo entre solicitudes
}