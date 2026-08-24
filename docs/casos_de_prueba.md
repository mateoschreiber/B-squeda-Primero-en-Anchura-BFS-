# Casos de prueba manuales

Ejecuta cada comando desde la carpeta principal del repositorio.

| Caso | Comando | Qué debes comprobar |
| --- | --- | --- |
| Demostración principal | `python -m junta_saneamiento` | Aparecen S1 a S7; la ruta a S7 es S1 → S2 → S4 → S7. |
| Otro origen | `python -m junta_saneamiento --origen S3 --destino S7` | S3 figura en el nivel 0. |
| Destino inexistente | `python -m junta_saneamiento --destino X` | Muestra `Error` y termina con código 2. |
| Archivo JSON inválido | `python -m junta_saneamiento --red ruta\archivo_invalido.json` | Muestra un error claro y termina con código 2. |
| Rotura en tanque | `python -m junta_saneamiento --escenario rotura-tanque` | Conserva la ruta S1 → S2 → S4 → S7. |
| Nueva toma S8 | `python -m junta_saneamiento --escenario rotura-toma-s8` | La ruta es S8 → S5 → S2 → S4 → S7. |
| Toma S9 aislada | `python -m junta_saneamiento --escenario toma-aislada` | S9 aparece en `No alcanzables`. |
| Conexión S2-S4 interrumpida | `python -m junta_saneamiento --escenario conexion-interrumpida` | S4 y S7 aparecen como no alcanzables. |
| Origen S99 | `python -m junta_saneamiento --escenario origen-inexistente` | Muestra que S99 no existe y termina con código 2. |
| Opciones incompatibles | `python -m junta_saneamiento --escenario rotura-tanque --origen S1` | Explica que las opciones no se pueden combinar y termina con código 2. |

Para la comprobación automática ejecuta `python -m unittest discover -s tests -v`. Deben aprobarse 13 pruebas. También se verifica que S8 sea bidireccional, que la red original siga limitada a S1-S7 y que la API de Python coincida con la consola.

Ejemplo desde Python:

```python
from junta_saneamiento import simular_toma_aislada

escenario = simular_toma_aislada()
assert "S9" in escenario.resultado.unreachable
```
