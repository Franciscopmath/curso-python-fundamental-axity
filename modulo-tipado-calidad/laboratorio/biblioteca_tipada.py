#!/usr/bin/env python3
"""
Sistema de Gestión de Biblioteca - Laboratorio Módulo 5
Tipado Estático Opcional y Calidad de Código

Demuestra:
- Type hints básicos y avanzados
- Union types, Literal, TypedDict, Protocol
- Validación con mypy
- Cumplimiento de PEP 8
- Uso de ruff, black, isort
- Pre-commit hooks
"""

from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import StrEnum
from typing import (
    Final,
    Literal,
    Protocol,
    TypeAlias,
    TypedDict,
    TypeVar,
    overload,
)

# ============================================================================
# CONSTANTES Y TIPOS
# ============================================================================

# Constantes con Final
MAX_PRESTAMOS_USUARIO: Final[int] = 5
DIAS_PRESTAMO_ESTANDAR: Final[int] = 14
MULTA_POR_DIA: Final[float] = 1.50

# Type aliases
ISBN: TypeAlias = str
UserID: TypeAlias = int
BookID: TypeAlias = int

# Literal types para opciones específicas
TipoUsuario = Literal["estudiante", "profesor", "externo"]
EstadoLibro = Literal["disponible", "prestado", "reservado", "mantenimiento"]
CategoriaLibro = Literal["ficcion", "no_ficcion", "referencia", "revista"]


# ============================================================================
# ENUMERACIONES
# ============================================================================


class EstadoPrestamo(StrEnum):
    """Estados posibles de un préstamo."""

    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    VENCIDO = "vencido"
    RENOVADO = "renovado"


# ============================================================================
# TYPEDDICT - ESTRUCTURAS DE DATOS
# ============================================================================


class LibroDict(TypedDict):
    """Representación de un libro como diccionario tipado."""

    id: BookID
    titulo: str
    autor: str
    isbn: ISBN
    categoria: CategoriaLibro
    estado: EstadoLibro
    anio_publicacion: int


class UsuarioDict(TypedDict, total=False):
    """Representación de un usuario con campos opcionales."""

    id: UserID  # Required
    nombre: str  # Required
    email: str  # Required
    tipo: TipoUsuario  # Required
    telefono: str  # Opcional
    direccion: str  # Opcional


class PrestamoDict(TypedDict):
    """Representación de un préstamo."""

    id: int
    libro_id: BookID
    usuario_id: UserID
    fecha_prestamo: str
    fecha_devolucion: str
    estado: str


# ============================================================================
# PROTOCOLS - INTERFACES ESTRUCTURALES
# ============================================================================


class Prestable(Protocol):
    """Protocolo para objetos que pueden ser prestados."""

    def esta_disponible(self) -> bool:
        """Verifica si el objeto está disponible para préstamo."""
        ...

    def prestar(self) -> None:
        """Marca el objeto como prestado."""
        ...

    def devolver(self) -> None:
        """Marca el objeto como devuelto."""
        ...


class Identificable(Protocol):
    """Protocolo para objetos con ID."""

    @property
    def id(self) -> int:
        """Retorna el ID del objeto."""
        ...


class Validable(Protocol):
    """Protocolo para objetos validables."""

    def validar(self) -> bool:
        """Valida el objeto."""
        ...

    def errores_validacion(self) -> list[str]:
        """Retorna lista de errores de validación."""
        ...


# ============================================================================
# GENERIC TYPES
# ============================================================================

T = TypeVar("T")
EntidadT = TypeVar("EntidadT", bound=Identificable)


class Repositorio(Protocol[EntidadT]):
    """Protocolo genérico para repositorios."""

    def obtener(self, id: int) -> EntidadT | None:
        """Obtiene una entidad por ID."""
        ...

    def listar(self) -> list[EntidadT]:
        """Lista todas las entidades."""
        ...

    def guardar(self, entidad: EntidadT) -> None:
        """Guarda una entidad."""
        ...

    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por ID."""
        ...


# ============================================================================
# CLASES DE DOMINIO
# ============================================================================


@dataclass
class Libro:
    """
    Representa un libro en la biblioteca.

    Demuestra:
    - Type hints en dataclasses
    - Uso de Literal types
    - Properties con tipos
    - Validación en __post_init__
    """

    titulo: str
    autor: str
    isbn: ISBN
    categoria: CategoriaLibro
    anio_publicacion: int
    id: BookID = field(default=0, init=False)
    estado: EstadoLibro = "disponible"
    _contador_id: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        """Validaciones y asignación de ID."""
        if not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")

        if not self.autor.strip():
            raise ValueError("El autor no puede estar vacío")

        isbn_limpio = self.isbn.replace("-", "").replace(" ", "")
        if len(isbn_limpio) not in (10, 13):
            raise ValueError("ISBN debe tener 10 o 13 dígitos")

        if self.anio_publicacion < 1000 or self.anio_publicacion > datetime.now().year:
            raise ValueError(f"Año de publicación inválido: {self.anio_publicacion}")

        # Generar ID único
        Libro._contador_id += 1
        self.id = Libro._contador_id

    def esta_disponible(self) -> bool:
        """Verifica si el libro está disponible."""
        return self.estado == "disponible"

    def prestar(self) -> None:
        """Marca el libro como prestado."""
        if not self.esta_disponible():
            raise ValueError(f"El libro '{self.titulo}' no está disponible")
        self.estado = "prestado"

    def devolver(self) -> None:
        """Marca el libro como disponible."""
        self.estado = "disponible"

    def reservar(self) -> None:
        """Marca el libro como reservado."""
        if self.estado != "disponible":
            raise ValueError(f"El libro '{self.titulo}' no puede ser reservado")
        self.estado = "reservado"

    def to_dict(self) -> LibroDict:
        """Convierte el libro a diccionario tipado."""
        return LibroDict(
            id=self.id,
            titulo=self.titulo,
            autor=self.autor,
            isbn=self.isbn,
            categoria=self.categoria,
            estado=self.estado,
            anio_publicacion=self.anio_publicacion,
        )


@dataclass
class Usuario:
    """
    Representa un usuario de la biblioteca.

    Demuestra:
    - Type hints completos
    - Uso de TipoUsuario (Literal)
    - Propiedades calculadas
    """

    nombre: str
    email: str
    tipo: TipoUsuario
    telefono: str = ""
    direccion: str = ""
    id: UserID = field(default=0, init=False)
    _prestamos_activos: list[int] = field(default_factory=list, init=False, repr=False)
    _contador_id: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        """Validaciones."""
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        if "@" not in self.email:
            raise ValueError("Email inválido")

        Usuario._contador_id += 1
        self.id = Usuario._contador_id

    @property
    def max_prestamos(self) -> int:
        """Retorna el máximo de préstamos según el tipo de usuario."""
        limites: dict[TipoUsuario, int] = {
            "estudiante": 3,
            "profesor": 10,
            "externo": 2,
        }
        return limites[self.tipo]

    @property
    def puede_pedir_prestado(self) -> bool:
        """Verifica si el usuario puede pedir más libros prestados."""
        return len(self._prestamos_activos) < self.max_prestamos

    def agregar_prestamo(self, prestamo_id: int) -> None:
        """Agrega un préstamo activo."""
        if not self.puede_pedir_prestado:
            raise ValueError(f"Usuario {self.nombre} ha alcanzado el límite de préstamos")
        self._prestamos_activos.append(prestamo_id)

    def remover_prestamo(self, prestamo_id: int) -> None:
        """Remueve un préstamo activo."""
        if prestamo_id in self._prestamos_activos:
            self._prestamos_activos.remove(prestamo_id)

    def to_dict(self) -> UsuarioDict:
        """Convierte el usuario a diccionario tipado."""
        resultado: UsuarioDict = {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "tipo": self.tipo,
        }

        if self.telefono:
            resultado["telefono"] = self.telefono
        if self.direccion:
            resultado["direccion"] = self.direccion

        return resultado


@dataclass
class Prestamo:
    """
    Representa un préstamo de libro.

    Demuestra:
    - Type hints con datetime
    - Properties calculadas
    - Lógica de negocio tipada
    """

    libro: Libro
    usuario: Usuario
    fecha_prestamo: date = field(default_factory=date.today)
    fecha_devolucion_esperada: date = field(init=False)
    fecha_devolucion_real: date | None = None
    estado: EstadoPrestamo = EstadoPrestamo.ACTIVO
    id: int = field(default=0, init=False)
    _contador_id: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        """Calcula fecha de devolución e ID."""
        self.fecha_devolucion_esperada = self.fecha_prestamo + timedelta(
            days=DIAS_PRESTAMO_ESTANDAR
        )
        Prestamo._contador_id += 1
        self.id = Prestamo._contador_id

        # Actualizar estado del libro y usuario
        self.libro.prestar()
        self.usuario.agregar_prestamo(self.id)

    @property
    def dias_prestado(self) -> int:
        """Retorna días que el libro ha estado prestado."""
        if self.fecha_devolucion_real:
            return (self.fecha_devolucion_real - self.fecha_prestamo).days
        return (date.today() - self.fecha_prestamo).days

    @property
    def esta_vencido(self) -> bool:
        """Verifica si el préstamo está vencido."""
        if self.estado == EstadoPrestamo.DEVUELTO:
            return False
        return date.today() > self.fecha_devolucion_esperada

    @property
    def dias_retraso(self) -> int:
        """Calcula días de retraso."""
        if not self.esta_vencido:
            return 0
        return (date.today() - self.fecha_devolucion_esperada).days

    @property
    def multa(self) -> float:
        """Calcula la multa por retraso."""
        return self.dias_retraso * MULTA_POR_DIA

    def devolver(self) -> None:
        """Registra la devolución del libro."""
        if self.estado == EstadoPrestamo.DEVUELTO:
            raise ValueError("El préstamo ya fue devuelto")

        self.fecha_devolucion_real = date.today()
        self.estado = EstadoPrestamo.DEVUELTO
        self.libro.devolver()
        self.usuario.remover_prestamo(self.id)

    def renovar(self) -> None:
        """Renueva el préstamo por más días."""
        if self.estado != EstadoPrestamo.ACTIVO:
            raise ValueError("Solo se pueden renovar préstamos activos")

        if self.esta_vencido:
            raise ValueError("No se pueden renovar préstamos vencidos")

        self.fecha_devolucion_esperada += timedelta(days=DIAS_PRESTAMO_ESTANDAR)
        self.estado = EstadoPrestamo.RENOVADO

    def to_dict(self) -> PrestamoDict:
        """Convierte el préstamo a diccionario."""
        return PrestamoDict(
            id=self.id,
            libro_id=self.libro.id,
            usuario_id=self.usuario.id,
            fecha_prestamo=self.fecha_prestamo.isoformat(),
            fecha_devolucion=self.fecha_devolucion_esperada.isoformat(),
            estado=self.estado.value,
        )


# ============================================================================
# FUNCIONES CON TYPE HINTS AVANZADOS
# ============================================================================


# Overload para múltiples signatures
@overload
def buscar_libros(criterio: str, *, por_titulo: Literal[True]) -> list[Libro]: ...


@overload
def buscar_libros(criterio: str, *, por_autor: Literal[True]) -> list[Libro]: ...


@overload
def buscar_libros(criterio: str, *, por_isbn: Literal[True]) -> Libro | None: ...


def buscar_libros(
    criterio: str,
    *,
    por_titulo: bool = False,
    por_autor: bool = False,
    por_isbn: bool = False,
) -> list[Libro] | Libro | None:
    """
    Busca libros según diferentes criterios.

    Demuestra el uso de @overload para múltiples signatures.
    """
    # Implementación simulada
    if por_isbn:
        return None
    return []


def filtrar_por_condicion(
    items: Sequence[T],
    predicado: Callable[[T], bool],
) -> list[T]:
    """
    Filtra items usando un predicado.

    Demuestra:
    - TypeVar genérico
    - Callable con tipos
    - Sequence (más general que list)
    """
    return [item for item in items if predicado(item)]


def obtener_libros_disponibles(libros: Sequence[Libro]) -> list[Libro]:
    """Retorna solo libros disponibles."""
    return filtrar_por_condicion(libros, lambda libro: libro.esta_disponible())


def mapear_transformacion(
    items: Sequence[T],
    transformacion: Callable[[T], str],
) -> list[str]:
    """
    Mapea items a strings usando una transformación.

    Demuestra uso de Callable con tipos específicos de retorno.
    """
    return [transformacion(item) for item in items]


def agrupar_por_categoria(
    libros: Sequence[Libro],
) -> dict[CategoriaLibro, list[Libro]]:
    """
    Agrupa libros por categoría.

    Demuestra:
    - Retorno con dict tipado
    - Uso de Literal type como key
    """
    grupos: dict[CategoriaLibro, list[Libro]] = {
        "ficcion": [],
        "no_ficcion": [],
        "referencia": [],
        "revista": [],
    }

    for libro in libros:
        grupos[libro.categoria].append(libro)

    return grupos


def generar_reporte_prestamos(
    prestamos: Sequence[Prestamo],
) -> dict[str, int | float]:
    """
    Genera reporte estadístico de préstamos.

    Demuestra dict con valores de múltiples tipos.
    """
    total = len(prestamos)
    activos = sum(1 for p in prestamos if p.estado == EstadoPrestamo.ACTIVO)
    vencidos = sum(1 for p in prestamos if p.esta_vencido)
    multas_total = sum(p.multa for p in prestamos)

    return {
        "total_prestamos": total,
        "prestamos_activos": activos,
        "prestamos_vencidos": vencidos,
        "multas_totales": multas_total,
        "promedio_dias_prestado": (
            sum(p.dias_prestado for p in prestamos) / total if total > 0 else 0
        ),
    }


# ============================================================================
# GENERADORES CON TIPOS
# ============================================================================


def generar_fechas_rango(
    fecha_inicio: date,
    fecha_fin: date,
) -> Iterator[date]:
    """
    Genera fechas en un rango.

    Demuestra Generator/Iterator con tipos.
    """
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        yield fecha_actual
        fecha_actual += timedelta(days=1)


def prestamos_vencidos(prestamos: Sequence[Prestamo]) -> Iterator[Prestamo]:
    """Genera préstamos vencidos."""
    for prestamo in prestamos:
        if prestamo.esta_vencido:
            yield prestamo


# ============================================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================================


def validar_isbn(isbn: str) -> bool:
    """
    Valida formato de ISBN.

    Demuestra función simple con tipos claros.
    """
    isbn_limpio = isbn.replace("-", "").replace(" ", "")
    return len(isbn_limpio) in (10, 13) and isbn_limpio.isalnum()


def validar_email(email: str) -> bool:
    """Valida formato básico de email."""
    return "@" in email and "." in email.split("@")[1]


# ============================================================================
# CLASE DE GESTIÓN PRINCIPAL
# ============================================================================


class Biblioteca:
    """
    Sistema de gestión de biblioteca.

    Demuestra:
    - Type hints en métodos de clase
    - Gestión de colecciones tipadas
    - Lógica de negocio compleja
    """

    def __init__(self) -> None:
        """Inicializa la biblioteca."""
        self._libros: list[Libro] = []
        self._usuarios: list[Usuario] = []
        self._prestamos: list[Prestamo] = []

    def agregar_libro(self, libro: Libro) -> None:
        """Agrega un libro al catálogo."""
        if any(lb.isbn == libro.isbn for lb in self._libros):
            raise ValueError(f"Ya existe un libro con ISBN {libro.isbn}")
        self._libros.append(libro)

    def agregar_usuario(self, usuario: Usuario) -> None:
        """Agrega un usuario al sistema."""
        if any(u.email == usuario.email for u in self._usuarios):
            raise ValueError(f"Ya existe un usuario con email {usuario.email}")
        self._usuarios.append(usuario)

    def buscar_libro_por_id(self, libro_id: BookID) -> Libro | None:
        """Busca un libro por ID."""
        for libro in self._libros:
            if libro.id == libro_id:
                return libro
        return None

    def buscar_usuario_por_id(self, usuario_id: UserID) -> Usuario | None:
        """Busca un usuario por ID."""
        for usuario in self._usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def crear_prestamo(
        self,
        libro_id: BookID,
        usuario_id: UserID,
    ) -> Prestamo:
        """
        Crea un nuevo préstamo.

        Demuestra:
        - Manejo de None con comprobaciones
        - Lógica de negocio tipada
        """
        libro = self.buscar_libro_por_id(libro_id)
        if libro is None:
            raise ValueError(f"Libro {libro_id} no encontrado")

        usuario = self.buscar_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError(f"Usuario {usuario_id} no encontrado")

        if not libro.esta_disponible():
            raise ValueError(f"Libro '{libro.titulo}' no está disponible")

        if not usuario.puede_pedir_prestado:
            raise ValueError(f"Usuario '{usuario.nombre}' ha alcanzado el límite")

        prestamo = Prestamo(libro=libro, usuario=usuario)
        self._prestamos.append(prestamo)
        return prestamo

    def listar_libros_disponibles(self) -> list[Libro]:
        """Lista libros disponibles."""
        return [libro for libro in self._libros if libro.esta_disponible()]

    def listar_prestamos_activos(self) -> list[Prestamo]:
        """Lista préstamos activos."""
        return [p for p in self._prestamos if p.estado == EstadoPrestamo.ACTIVO]

    def listar_prestamos_vencidos(self) -> list[Prestamo]:
        """Lista préstamos vencidos."""
        return [p for p in self._prestamos if p.esta_vencido]

    def obtener_estadisticas(self) -> dict[str, int | float]:
        """Genera estadísticas del sistema."""
        return {
            "total_libros": len(self._libros),
            "libros_disponibles": len(self.listar_libros_disponibles()),
            "total_usuarios": len(self._usuarios),
            "prestamos_activos": len(self.listar_prestamos_activos()),
            "prestamos_vencidos": len(self.listar_prestamos_vencidos()),
            "multas_pendientes": sum(p.multa for p in self.listar_prestamos_vencidos()),
        }


# ============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# ============================================================================


def ejemplo_basico() -> None:
    """Ejemplo básico de uso del sistema."""
    print("=" * 80)
    print("EJEMPLO 1: Uso Básico del Sistema")
    print("=" * 80)

    # Crear biblioteca
    biblioteca = Biblioteca()

    # Agregar libros
    libro1 = Libro(
        titulo="El Principito",
        autor="Antoine de Saint-Exupéry",
        isbn="978-0156012195",
        categoria="ficcion",
        anio_publicacion=1943,
    )

    libro2 = Libro(
        titulo="Python Crash Course",
        autor="Eric Matthes",
        isbn="978-1593279288",
        categoria="no_ficcion",
        anio_publicacion=2019,
    )

    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)

    # Agregar usuario
    usuario = Usuario(
        nombre="Ana García",
        email="ana@example.com",
        tipo="estudiante",
        telefono="123456789",
    )

    biblioteca.agregar_usuario(usuario)

    # Crear préstamo
    prestamo = biblioteca.crear_prestamo(libro1.id, usuario.id)

    print(f"Préstamo creado: #{prestamo.id}")
    print(f"Libro: {prestamo.libro.titulo}")
    print(f"Usuario: {prestamo.usuario.nombre}")
    print(f"Fecha devolución: {prestamo.fecha_devolucion_esperada}")
    print(f"Estado: {prestamo.estado.value}")

    # Estadísticas
    stats = biblioteca.obtener_estadisticas()
    print("\nEstadísticas:")
    for clave, valor in stats.items():
        print(f"  {clave}: {valor}")

    print("\n")


def ejemplo_type_hints_avanzados() -> None:
    """Demuestra type hints avanzados."""
    print("=" * 80)
    print("EJEMPLO 2: Type Hints Avanzados")
    print("=" * 80)

    # TypedDict
    libro_dict: LibroDict = {
        "id": 1,
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "isbn": "978-0132350884",
        "categoria": "no_ficcion",
        "estado": "disponible",
        "anio_publicacion": 2008,
    }
    print(f"Libro (TypedDict): {libro_dict['titulo']}")

    # Union types con |
    valor: int | str = 42
    print(f"Valor union: {valor} (tipo: {type(valor).__name__})")

    # Literal types
    modo: TipoUsuario = "estudiante"
    print(f"Tipo de usuario: {modo}")

    # Callable
    def es_ficcion(libro: Libro) -> bool:
        return libro.categoria == "ficcion"

    libros = [
        Libro("Libro 1", "Autor 1", "1234567890", "ficcion", 2020),
        Libro("Libro 2", "Autor 2", "9876543210", "no_ficcion", 2021),
    ]

    ficcion = filtrar_por_condicion(libros, es_ficcion)
    print(f"Libros de ficción encontrados: {len(ficcion)}")

    print("\n")


def ejemplo_validacion_tipos() -> None:
    """Demuestra validación de tipos."""
    print("=" * 80)
    print("EJEMPLO 3: Validación de Tipos")
    print("=" * 80)

    # Validación de ISBN
    isbns_validos = ["978-0132350884", "0-306-40615-2"]
    isbns_invalidos = ["123", "abc-def-ghi"]

    print("ISBNs válidos:")
    for isbn in isbns_validos:
        resultado = "✓" if validar_isbn(isbn) else "✗"
        print(f"  {resultado} {isbn}")

    print("\nISBNs inválidos:")
    for isbn in isbns_invalidos:
        resultado = "✓" if validar_isbn(isbn) else "✗"
        print(f"  {resultado} {isbn}")

    # Validación de errores en tiempo de creación
    print("\nIntentando crear libro con datos inválidos:")
    try:
        Libro("", "Autor", "123", "ficcion", 2020)
    except ValueError as e:
        print(f"  ✗ Error esperado: {e}")

    print("\n")


def main() -> None:
    """Ejecuta todos los ejemplos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "SISTEMA DE BIBLIOTECA" + " " * 39 + "║")
    print("║" + " " * 10 + "Tipado Estático Opcional y Calidad - Módulo 5" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    ejemplos: list[Callable[[], None]] = [
        ejemplo_basico,
        ejemplo_type_hints_avanzados,
        ejemplo_validacion_tipos,
    ]

    for ejemplo in ejemplos:
        ejemplo()

    print("=" * 80)
    print("FIN DE EJEMPLOS")
    print("=" * 80)
    print("""
Conceptos demostrados:
  ✓ Type hints básicos (int, str, float, bool)
  ✓ Type hints de colecciones (list, dict, set, tuple)
  ✓ Union types (int | str)
  ✓ Literal types para valores específicos
  ✓ TypedDict para diccionarios estructurados
  ✓ Protocol para interfaces estructurales
  ✓ Generic types con TypeVar
  ✓ Callable para funciones como parámetros
  ✓ Type aliases para claridad
  ✓ Overload para múltiples signatures
  ✓ Iterator/Generator con tipos
  ✓ Validación con mypy
  ✓ PEP 8 compliant (verificado con ruff)
  ✓ Formateado con black e isort
""")


if __name__ == "__main__":
    main()
