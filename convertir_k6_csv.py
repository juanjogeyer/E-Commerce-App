import json
import csv
from collections import defaultdict

archivo_json = 'resultado.json'
archivo_csv = 'resultado.csv'

# Función para ordenar las métricas por el nombre
def ordenar_metricas(metricas):
    return sorted(metricas, key=lambda x: x[0])

# Creamos un diccionario para almacenar las métricas
metricas_dict = defaultdict(list)

# Abrimos el archivo CSV para escribir
with open(archivo_csv, 'w', newline='') as csv_file:
    escritor = csv.writer(csv_file)
    
    # Escribimos los encabezados
    encabezados = ['Métrica', 'Tipo', 'Valor', 'Tiempo', 'Escenario']
    escritor.writerow(encabezados)

    # Abrimos el archivo JSON para leer las métricas
    with open(archivo_json, 'r') as json_file:
        for linea in json_file:
            try:
                datos = json.loads(linea)
                
                # Extraemos los datos de la métrica
                metric = datos.get('metric', 'N/A')
                tipo = datos.get('type', 'N/A')
                value = datos.get('data', {}).get('value', 'N/A')
                time = datos.get('data', {}).get('time', 'N/A')
                escenario = datos.get('data', {}).get('tags', {}).get('scenario', 'N/A')

                # Almacenamos los datos en un diccionario agrupado por nombre de la métrica
                metricas_dict[metric].append((tipo, value, time, escenario))

            except json.JSONDecodeError as e:
                print(f"Error procesando línea: {e}")

    # Ordenamos las métricas por nombre
    metricas_ordenadas = ordenar_metricas(metricas_dict.items())

    # Escribimos las métricas ordenadas en el archivo CSV
    for metric, valores in metricas_ordenadas:
        for valor in valores:
            tipo, value, time, escenario = valor
            escritor.writerow([metric, tipo, value, time, escenario])

print(f"Archivo CSV generado: {archivo_csv}")
