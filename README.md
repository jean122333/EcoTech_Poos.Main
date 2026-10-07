# EcoTech – Modelo de clases y persistencia (POO)

Proyecto de Programación Orientada a Objetos (Unidad 2). Implementa en Python las
clases del diagrama UML (`Empleado`, `Departamento`, `Proyecto`, `RegistroTiempo`)
y un CRUD de empleados con menú de consola. Funciona con SQLite o MariaDB/MySQL,
según lo que se configure en el archivo `.env`.

## Estructura

```
EcoTech_Poos.Main/
├── requirements.txt
├── .env.example          # plantilla de configuración (se copia como .env)
├── .gitignore
└── src/
    ├── main.py           # menú de consola y coordinación
    ├── dominio/          # clases del UML (no conocen SQL)
    │   ├── empleado.py
    │   ├── departamento.py
    │   ├── proyecto.py
    │   └── registroTiempo.py
    └── persistencia/     # acceso a la base de datos
        ├── conexion.py   # abre SQLite o MariaDB según DB_ENGINE
        ├── crear_bd.py   # crea la tabla según el motor
        └── empleado_dao.py  # INSERT, SELECT, UPDATE y DELETE
```

## Responsabilidades

- `dominio/`: clases del problema, con validaciones. No conocen SQLite ni MariaDB.
- `persistencia/`: conexión, creación de tablas y DAO. Aquí está todo el SQL.
- `main.py`: menú, validación de entradas y mensajes al usuario. No contiene SQL ni credenciales.
- `.env`: selecciona el motor y guarda la configuración local (no se sube al repositorio).

## Requisitos

- Python 3.10 o superior
- Para MariaDB: XAMPP (MySQL/MariaDB y phpMyAdmin) o cualquier servidor compatible

## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto:
```bash
git clone https://github.com/jean122333/EcoTech_Poos.Main.git
cd EcoTech_Poos.Main
```
2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```
3. Crear el archivo `.env` a partir de la plantilla:
```bash
cp .env.example .env        # en CMD de Windows: copy .env.example .env
```
4. Elegir el motor en `.env`:

SQLite (no necesita servidor):
```
DB_ENGINE=sqlite
DB_NAME=ecotech.db
```

MariaDB (iniciar MySQL desde XAMPP antes de ejecutar):
```
DB_ENGINE=mariadb
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=ecotech
```
5. Ejecutar el programa:
```bash
python src/main.py
```

La base de datos (en MariaDB) y la tabla `empleado` se crean automáticamente si no existen.
Si se cambia de motor, los datos no se comparten: cada motor guarda los suyos.

## Menú

```
1. Registrar empleado
2. Listar empleados
3. Buscar empleado (por ID o por correo)
4. Actualizar empleado
5. Eliminar empleado
6. Demo de relaciones
0. Salir
```

## Notas de diseño

- **Un DAO, dos motores:** `conexion.py` informa el motor y el marcador SQL (`?` en SQLite,
  `%s` en MariaDB); el dominio y `main.py` no cambian.
- **Consultas parametrizadas** en el DAO para evitar inyección SQL.
- **Identidad del objeto:** un `Empleado` nuevo comienza con `id=None`; la base de datos
  genera el id y el DAO lo recupera con `cursor.lastrowid`.
- **Manejo de errores:** las escrituras usan `try/except/finally` con `rollback` y cierre de
  conexión. El usuario ve un mensaje seguro; el detalle técnico queda en `ecotech.log`.
- **Resultados normales vs. excepciones:** buscar un id inexistente devuelve `None` y
  eliminar un id inexistente devuelve `False`; no son excepciones.
- **Credenciales fuera del código:** se leen desde `.env` con `python-dotenv`.
- **Relación "Consulta"** (Proyecto–Departamento, 1 a 1) del diagrama original:
  no se implementó por decisión del equipo.

