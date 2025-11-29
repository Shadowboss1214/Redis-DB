import csv
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

start_time = time.time()

nombre_archivo = 'spotify_history.csv'

with open(nombre_archivo, encoding='utf-8') as f:
    reader = csv.DictReader(f)

    pipe = r.pipeline()

    count = 0
    for i, row in enumerate(reader):

        key = f"repro:{i}"
        pipe.hset(key, mapping=row)
        # Cada 2000 registros, ejecutamos el paquete y limpiamos la tubería
        if (i + 1) % 2000 == 0:
            pipe.execute()
            print(f"Procesados {i+1} registros...")

        count = i
    # Ejecutamos cualquier registro que haya quedado pendiente al final
    pipe.execute()

end_time = time.time()
print(f"¡Éxito! Se cargaron {count+1} registros en {end_time - start_time:.2f} segundos.")
