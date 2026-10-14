# persistencia/crear_bd.py
from persistencia.conexion import abrir_conexion, obtener_motor

# Tipos de columna según el motor. Así se escribe cada CREATE TABLE una sola vez.
_TIPOS = {
    "sqlite": {
        "pk": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "int": "INTEGER",
        "texto_corto": "TEXT",
        "texto_medio": "TEXT",
        "texto_largo": "TEXT",
        "dinero": "REAL",
        "horas": "REAL",
        "fecha": "TEXT",
        "final": "",
    },
    "mysql": {
        "pk": "INT PRIMARY KEY AUTO_INCREMENT",
        "int": "INT",
        "texto_corto": "VARCHAR(100)",
        "texto_medio": "VARCHAR(150)",
        "texto_largo": "TEXT",
        "dinero": "DECIMAL(10,2)",
        "horas": "DECIMAL(5,2)",
        "fecha": "DATE",
        # InnoDB es el motor que soporta claves foráneas
        "final": " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
    },
}

# Orden importa: primero las tablas a las que otras hacen referencia (claves foráneas).
_TABLAS = [
    # Departamento 1 ── 0..* Empleado: la clave foránea queda en empleado
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id_departamento {pk},
        nombre {texto_corto} NOT NULL UNIQUE,
        gerente {texto_corto} NOT NULL
    ){final}
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id_empleado {pk},
        nombre {texto_corto} NOT NULL,
        correo {texto_medio} NOT NULL UNIQUE,
        salario {dinero} NOT NULL,
        departamento_id {int} NULL,
        FOREIGN KEY (departamento_id) REFERENCES departamento (id_departamento)
            ON DELETE SET NULL
    ){final}
    """,
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id_proyecto {pk},
        nombre {texto_corto} NOT NULL UNIQUE,
        fecha_inicio {fecha} NOT NULL,
        descripcion {texto_largo} NOT NULL
    ){final}
    """,
    # Empleado 0..* ── 0..* Proyecto: tabla intermedia con clave primaria compuesta
    """
    CREATE TABLE IF NOT EXISTS empleado_proyecto (
        empleado_id {int} NOT NULL,
        proyecto_id {int} NOT NULL,
        PRIMARY KEY (empleado_id, proyecto_id),
        FOREIGN KEY (empleado_id) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto (id_proyecto) ON DELETE CASCADE
    ){final}
    """,
    # Empleado 1 ── 0..* RegistroTiempo 0..* ── 1 Proyecto
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id_registro {pk},
        fecha {fecha} NOT NULL,
        horas_trabajadas {horas} NOT NULL,
        descripcion {texto_largo} NOT NULL,
        empleado_id {int} NOT NULL,
        proyecto_id {int} NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto (id_proyecto) ON DELETE SET NULL
    ){final}
    """,
]


def _tiene_columna(cursor, tabla, columna):
    if obtener_motor() == "sqlite":
        cursor.execute(f"PRAGMA table_info({tabla})")
        return any(fila[1] == columna for fila in cursor.fetchall())
    cursor.execute(f"SHOW COLUMNS FROM {tabla} LIKE '{columna}'")
    return cursor.fetchone() is not None


def _migrar_empleado(cursor):
    """Bases creadas con la versión anterior no tienen empleado.departamento_id."""
    if _tiene_columna(cursor, "empleado", "departamento_id"):
        return
    if obtener_motor() == "sqlite":
        cursor.execute(
            "ALTER TABLE empleado ADD COLUMN departamento_id INTEGER "
            "REFERENCES departamento (id_departamento) ON DELETE SET NULL"
        )
    else:
        cursor.execute(
            "ALTER TABLE empleado ADD COLUMN departamento_id INT NULL, "
            "ADD CONSTRAINT fk_empleado_departamento FOREIGN KEY (departamento_id) "
            "REFERENCES departamento (id_departamento) ON DELETE SET NULL"
        )


def crear_tablas():
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        tipos = _TIPOS[obtener_motor()]

        for plantilla in _TABLAS:
            cursor.execute(plantilla.format(**tipos))

        _migrar_empleado(cursor)
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")