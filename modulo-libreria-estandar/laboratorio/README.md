# Laboratorio: Procesador de Ventas

Sistema de procesamiento de ventas que lee datos de CSV, calcula métricas y exporta resultados a JSON con logging completo.

## Objetivos

Este laboratorio implementa:

1. **pathlib**: Manejo moderno de rutas y archivos
2. **CSV**: Lectura y procesamiento de datos tabulares
3. **JSON**: Exportación de métricas y resultados
4. **datetime**: Procesamiento de fechas y cálculos temporales
5. **logging**: Sistema completo con niveles DEBUG, INFO, WARNING, ERROR, CRITICAL
6. **Métricas**: Cálculo de estadísticas y agregaciones
7. **Dataclasses**: Modelado de datos con validación

## Estructura del Proyecto

```
laboratorio/
├── data/
│   └── ventas_2024.csv          # Datos de entrada (50 registros)
├── output/
│   └── metricas_ventas.json     # Resultados exportados
├── logs/
│   └── procesador_ventas.log    # Archivo de logs
├── procesador_ventas.py          # Script principal
├── pyproject.toml                # Configuración Poetry
└── README.md                     # Este archivo
```

## Instalación

```bash
cd modulo-libreria-estandar/laboratorio
poetry install
poetry shell
```

## Uso

### Ejecutar el procesador

```bash
python procesador_ventas.py
```

**Salida esperada:**
1. Resumen en consola con métricas principales
2. Archivo JSON con métricas completas en `output/metricas_ventas.json`
3. Archivo de logs detallados en `logs/procesador_ventas.log`

## Características Implementadas

### 1. Lectura de CSV

```python
def leer_csv_ventas(archivo_csv: Path) -> list[Venta]:
    """Lee CSV y retorna lista de objetos Venta."""
    with archivo_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            venta = Venta(
                fecha=datetime.strptime(fila["fecha"], "%Y-%m-%d"),
                producto=fila["producto"],
                # ...
            )
```

**Características:**
- Usa `csv.DictReader` para acceso por nombre de columna
- Validación de datos con manejo de errores
- Logging de errores por línea
- Conversión automática de tipos

### 2. Modelo de Datos

```python
@dataclass
class Venta:
    fecha: datetime
    producto: str
    cantidad: int
    precio_unitario: Decimal
    # ...

    @property
    def total(self) -> Decimal:
        return Decimal(self.cantidad) * self.precio_unitario
```

**Características:**
- Uso de `Decimal` para precisión monetaria
- Properties calculadas (total, mes, trimestre)
- Validación en `__post_init__`
- Conversión a diccionario para JSON

### 3. Cálculo de Métricas

El sistema calcula automáticamente:

- **Métricas básicas**:
  - Total de ventas
  - Cantidad de transacciones
  - Ticket promedio
  - Venta mínima y máxima
  - Productos únicos vendidos

- **Agregaciones**:
  - Ventas por categoría
  - Ventas por región
  - Ventas por mes
  - Top 10 productos
  - Top 10 vendedores

### 4. Sistema de Logging

Configuración con múltiples niveles y destinos:

```python
logger = configurar_logging(nivel="DEBUG", archivo_log=Path("logs/app.log"))

logger.debug("Detalle de depuración")      # Solo en archivo
logger.info("Operación exitosa")           # Consola y archivo
logger.warning("Advertencia")              # Consola y archivo
logger.error("Error recuperable")          # Consola y archivo
logger.critical("Error crítico")           # Consola y archivo
```

**Características del logging:**
- Handler de consola (nivel INFO)
- Handler de archivo (nivel DEBUG)
- Rotación automática (10 MB, 5 backups)
- Formato detallado con timestamp, archivo y línea
- Logging de excepciones con traceback

### 5. Exportación a JSON

```python
{
  "metadata": {
    "generado_en": "2026-04-28T12:00:00",
    "total_registros": 50,
    "version": "1.0"
  },
  "metricas": {
    "resumen": {
      "total_ventas": 50000.00,
      "cantidad_transacciones": 50,
      "ticket_promedio": 1000.00
    },
    "por_categoria": { ... },
    "por_region": { ... },
    "top_productos": [ ... ]
  },
  "ventas": [ ... ]
}
```

### 6. Filtrado de Datos

```python
# Filtrar por categoría
ventas_electronica = filtrar_ventas(ventas, categoria="Electrónica")

# Filtrar por rango de fechas
ventas_trimestre = filtrar_ventas(
    ventas,
    fecha_inicio=datetime(2024, 7, 1),
    fecha_fin=datetime(2024, 9, 30)
)

# Múltiples filtros
ventas_filtradas = filtrar_ventas(
    ventas,
    categoria="Ropa",
    region="Norte",
    fecha_inicio=datetime(2024, 1, 1)
)
```

## Ejemplos de Salida

### Consola

```
================================================================================
                         RESUMEN DE VENTAS
================================================================================

Periodo: 2024-01-15 a 2024-10-20
Total de ventas: $68,547.35
Transacciones: 50
Ticket promedio: $1,370.95
Venta mínima: $149.70
Venta máxima: $2,999.98
Productos únicos: 50

--------------------------------------------------------------------------------
VENTAS POR CATEGORÍA
--------------------------------------------------------------------------------
Electrónica          $ 15,649.62  ( 22.8%)
Ropa                 $ 14,199.25  ( 20.7%)
Alimentos            $  9,487.80  ( 13.8%)
Libros               $  6,523.93  (  9.5%)
Hogar                $  4,987.75  (  7.3%)

--------------------------------------------------------------------------------
TOP 5 PRODUCTOS
--------------------------------------------------------------------------------
1. Laptop Dell XPS 13                $ 2,599.98
2. Cámara Canon                      $ 2,999.98
3. Impresora HP                      $ 1,199.96
```

### Archivo de Logs

```
2026-04-28 12:00:00 - procesador_ventas - INFO - procesador_ventas.py:450 - Iniciando procesador de ventas
2026-04-28 12:00:00 - procesador_ventas - INFO - procesador_ventas.py:460 - Paso 1: Leyendo datos de CSV
2026-04-28 12:00:00 - procesador_ventas - INFO - procesador_ventas.py:185 - Leyendo archivo CSV: data/ventas_2024.csv
2026-04-28 12:00:00 - procesador_ventas - DEBUG - procesador_ventas.py:215 - Venta procesada: 20240115-LAP - Laptop Dell XPS 13 (Total: $2599.98)
...
2026-04-28 12:00:00 - procesador_ventas - INFO - procesador_ventas.py:234 - CSV procesado: 50 ventas exitosas, 0 errores
2026-04-28 12:00:00 - procesador_ventas - INFO - procesador_ventas.py:251 - Calculando métricas de 50 ventas
2026-04-28 12:00:00 - procesador_ventas - DEBUG - procesador_ventas.py:272 - Total ventas: $68547.35
2026-04-28 12:00:00 - procesador_ventas - INFO - procesador_ventas.py:319 - Métricas calculadas exitosamente
```

## Comandos Útiles

```bash
# Ejecutar procesador
python procesador_ventas.py

# Ver logs en tiempo real
tail -f logs/procesador_ventas.log

# Verificar JSON generado
cat output/metricas_ventas.json | python -m json.tool

# Contar líneas en CSV
wc -l data/ventas_2024.csv

# Ver estructura de archivos
tree -L 2
```

## Verificación de Calidad

```bash
# Verificar código
poetry run ruff check procesador_ventas.py

# Formatear
poetry run black procesador_ventas.py
poetry run isort procesador_ventas.py

# Type checking (opcional, mypy tiene issues conocidos)
# poetry run mypy procesador_ventas.py
```

## Extensiones Propuestas

1. **Agregar argumentos CLI**: Usar `argparse` para especificar archivos y filtros
2. **Exportar a CSV**: Agregar función para exportar métricas a CSV
3. **Gráficos**: Usar matplotlib para visualizar métricas
4. **Tests**: Crear tests unitarios con pytest
5. **Configuración externa**: Leer configuración de archivo YAML
6. **Más formatos**: Soportar Excel, Parquet, etc.
7. **Base de datos**: Guardar métricas en SQLite
8. **API**: Exponer métricas vía Flask/FastAPI

## Conceptos Demostrados

- ✅ pathlib para rutas multiplataforma
- ✅ Context managers (with) para archivos
- ✅ CSV con DictReader para lectura estructurada
- ✅ JSON con indent y ensure_ascii=False
- ✅ datetime para parsing y cálculos
- ✅ Decimal para precisión monetaria
- ✅ logging con múltiples handlers y niveles
- ✅ RotatingFileHandler para rotación de logs
- ✅ dataclasses con properties y validación
- ✅ Type hints completos
- ✅ Manejo robusto de errores
- ✅ Agregaciones y estadísticas
- ✅ Filtrado de datos

## Recursos

- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [csv](https://docs.python.org/3/library/csv.html)
- [json](https://docs.python.org/3/library/json.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [logging](https://docs.python.org/3/library/logging.html)
- [decimal](https://docs.python.org/3/library/decimal.html)

## Notas

- El código usa Python 3.12 con type hints completos
- Cumple 100% con PEP 8
- Logging configurado para desarrollo (DEBUG en archivo)
- Usa Decimal para evitar errores de redondeo en cálculos monetarios
- Manejo robusto de errores en lectura de CSV
