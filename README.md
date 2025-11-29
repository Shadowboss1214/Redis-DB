# Redis-DB
## ¿En que consiste?
Este dataset es un registro histórico de reproducciones de Spotify (streaming history). Contiene datos detallados sobre qué canciones escuchó un usuario, cuándo, dónde y cómo interactuó con ellas (si las saltó, si las escuchó en aleatorio, etc.).

Cubre un periodo de más de 11 años, desde julio de 2013 hasta diciembre de 2024, con un total de casi 150,000 registros (reproducciones).

## Diccionario de datos del dataset
- **spotify_track_uri**: Spotify URI que identifica de forma única cada pista en el formato `spotify:track:<base-62 string>`
- **ts**: Marca de tiempo (Timestamp) que indica cuándo la pista dejó de reproducirse en UTC (Coordinated Universal Time)
- **platform**: Plataforma utilizada para reproducir la pista
- **ms_played**: Número de milisegundos que se reprodujo la pista
- **track_name**: Nombre de la pista
- **artist_name**: Nombre del artista
- **album_name**: Nombre del álbum
- **reason_start**: Razón por la que la pista comenzó
- **reason_end**: Razón por la que la pista terminó
- **shuffle**: `TRUE` o `FALSE` dependiendo de si se usó el modo aleatorio al reproducir la pista
- **skipped**: `TRUE` o `FALSE` dependiendo de si el usuario saltó a la siguiente canción

## Modelado de dataset

## Herramientas
Se utilizaron principalmente herramientas como Docker en Ubuntu, ya que Redis está diseñado para ejecutarse de manera óptima en sistemas basados en Linux. El uso de contenedores permitió crear un entorno aislado y reproducible, facilitando la instalación y configuración del servidor sin necesidad de hacerlo directamente en la máquina anfitriona. Además, se empleó el Redis Workbench para verificar la conectividad con la base de datos y ejecutar consultas de manera interactiva, aunque cabe destacar que Redis puede integrarse fácilmente en lenguajes de programación de alto nivel como C# o Python, lo que ofrece gran flexibilidad para el desarrollo de aplicaciones. El servidor se configuró de manera local debido a las limitaciones de almacenamiento en la nube: la plataforma de Redis imponía un límite de 30 MB, mientras que el dataset utilizado tiene un tamaño aproximado de 58 MB, lo que hizo inviable su carga en el servicio remoto. Por esta razón, se optó por manejarlo en un entorno local, garantizando un mejor control sobre los recursos y la disponibilidad de los datos. Finalmente, es importante señalar que la conexión a la base de datos puede realizarse directamente desde el contenedor de Docker sin necesidad de utilizar el Workbench, lo que permite un flujo de trabajo más ligero y automatizado en escenarios donde se busca integrar Redis con aplicaciones externas o scripts personalizados.

## Importación de datos
Como son muchos datos, hacerlo manual o con Excel sería imposible (Excel se trabaría). La forma profesional y rápida es usar un pequeño script de Python (ya proporcionado en la carpeta Proy_E1) que "lea" tu archivo y lo "inyecte" en Redis usando una técnica llamada Pipeline, que hace que la carga tarde segundos en lugar de horas.

Paso 1: Localice el script de Python
Ingrese en la carpeta Proy_E1, ya dentro de ella se encontrará con Spotify_Dataset.py

Paso 2: Prepare su entorno 
En su editor de código de confianza ejecute en la terminal el siguiente comando 
pip install Redis

Paso 3: Ejecute 
Una vez ya instalado todo y teniendo el script solo ejecútelo y verá como se inyectan todos los datos a Redis.

## Operaciones CRUD en Redis

### 🟢 CREATE (Crear)
- **HSET repro:nueva01 track_name "Flowers" artist_name "Miley Cyrus" ms_played "320000" platform "iOS"**  
  Crea un nuevo *hash* llamado `repro:nueva01` con varios campos (nombre de la canción, artista, duración en milisegundos y plataforma).

- **HSETNX repro:nueva01 track_name "Flowers" "Este valor no se guardará si la clave ya existe"**  
  Inserta un campo en el hash solo si no existe previamente. Si ya existe, no lo sobrescribe.

- **RPUSH cola:fiesta "repro:nueva01"**  
  Inserta el valor `"repro:nueva01"` al final de la lista `cola:fiesta`.

- **SADD artistas:favoritos "The Beatles" "The Killers" "Miley Cyrus"**  
  Agrega varios elementos a un conjunto llamado `artistas:favoritos`. Los conjuntos no permiten duplicados.

- **ZADD ranking:duracion 320000 "Flowers" 185000 "Yesterday"**  
  Inserta elementos en un *sorted set* (`ranking:duracion`) con puntuaciones asociadas (duración en ms).

---

### 🔵 READ (Leer)
- **HGETALL repro:1**  
  Obtiene todos los campos y valores del hash `repro:1`.

- **HMGET repro:1 artist_name track_name**  
  Devuelve solo los valores de los campos `artist_name` y `track_name` del hash `repro:1`.

- **HKEYS repro:1**  
  Lista todas las claves (nombres de campos) dentro del hash `repro:1`.

- **LRANGE cola:fiesta 0 -1**  
  Devuelve todos los elementos de la lista `cola:fiesta` (del índice 0 al último).

- **SISMEMBER artistas:favoritos "Bad Bunny"**  
  Verifica si `"Bad Bunny"` pertenece al conjunto `artistas:favoritos`.

---

### 🟠 UPDATE (Actualizar)
- **HSET repro:nueva01 platform "Windows 11"**  
  Actualiza el campo `platform` del hash `repro:nueva01` con el valor `"Windows 11"`.

- **HINCRBY repro:nueva01 ms_played 5000**  
  Incrementa en 5000 el valor numérico del campo `ms_played`.

- **RENAME repro:nueva01 repro:200000**  
  Cambia el nombre de la clave `repro:nueva01` a `repro:200000`.

- **LSET cola:fiesta 0 "repro:reemplazo"**  
  Modifica el primer elemento (índice 0) de la lista `cola:fiesta` y lo reemplaza por `"repro:reemplazo"`.

- **EXPIRE repro:200000 60**  
  Define un tiempo de expiración de 60 segundos para la clave `repro:200000`.

---

### 🔴 DELETE (Eliminar)
- **DEL repro:200000**  
  Elimina completamente la clave `repro:200000` y sus datos asociados.

- **HDEL repro:1 reason_start**  
  Borra solo el campo `reason_start` dentro del hash `repro:1`.

- **LPOP cola:fiesta**  
  Elimina y devuelve el primer elemento de la lista `cola:fiesta`.

- **SREM artistas:favoritos "The Beatles"**  
  Elimina `"The Beatles"` del conjunto `artistas:favoritos`.

- **FLUSHDB**  
  Borra todas las claves y datos de la base de datos actual. ⚠️ (acción destructiva).

