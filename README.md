# Redis-DB
## ¿En que consiste?
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

