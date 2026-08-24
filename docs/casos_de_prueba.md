# Casos de prueba manuales

Ejecuta cada comando desde la carpeta principal del repositorio.

| Caso | Comando | Qué debes comprobar |
| --- | --- | --- |
| Demostración principal | `python -m junta_saneamiento` | Aparecen S1 a S7; la ruta a S7 es S1 → S2 → S4 → S7. |
| Otro origen | `python -m junta_saneamiento --origen S3 --destino S7` | S3 figura en el nivel 0. |
| Destino inexistente | `python -m junta_saneamiento --destino X` | Muestra `Error` y termina con código 2. |
| Archivo JSON inválido | `python -m junta_saneamiento --red ruta\archivo_invalido.json` | Muestra un error claro y termina con código 2. |

Para la comprobación automática ejecuta `python -m unittest discover -s tests -v`. Las pruebas también verifican ciclos, nodos aislados, referencias inválidas y un orden de vecinos inconsistente.
