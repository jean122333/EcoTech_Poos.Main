# EcoTech – Modelo de clases y persistencia (POO)

Proyecto de Programación Orientada a Objetos (Unidad 2). Implementa en Python las
clases del diagrama UML (`Empleado`, `Departamento`, `Proyecto`, `RegistroTiempo`)
y guarda los empleados en una base de datos MySQL local administrada con phpMyAdmin.

## Estructura

```
Ecotech_poos.main/
├── requirements.txt
├── .env.example          ← plantilla de configuración (se copia como .env)
└── src/
    ├── main.py           ← prueba de conexión + inserción de 2 empleados
    ├── dominio/          ← clases del UML
    │   ├── empleado.py
    │   ├── departamento.py
    │   ├── proyecto.py
    │   └── registroTiempo.py
    └── persistencia/     ← acceso a la base de datos
        ├── conexion.py
        ├── crear_bd.py
        └── empleado_dao.py
```

## Requisitos

- Python 3.10 o superior
- XAMPP (MySQL y phpMyAdmin) o cualquier servidor MySQL local

## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto:
```bash
   git clone https://github.com/jean122333/EcoTech_Poos.Main.git
   cd EcoTech_Poos.Main/Ecotech_poos.main
```
2. Instalar las dependencias:
```bash
   pip install -r requirements.txt
```
3. Crear el archivo `.env` a partir de la plantilla y ajustar usuario, contraseña y puerto si es necesario:
```bash
   cp .env.example .env        # en CMD de Windows: copy .env.example .env
```
4. Iniciar **MySQL** desde el panel de XAMPP, abrir phpMyAdmin, ir a la pestaña **SQL** y ejecutar:
```sql
   CREATE DATABASE ecotech CHARACTER SET utf8mb4;
```
5. Ejecutar el programa:
```bash
   python src/main.py
```

Salida esperada (la primera vez):

```
Conexión exitosa (mysql).
Insertado: [1] Ana Torres - $850,000
Insertado: [2] Luis Pérez - $920,000
...
```

Si se ejecuta de nuevo, los empleados aparecen como "Ya existía" y no se duplican.
Si no existe el archivo `.env`, el programa usa SQLite como respaldo y lo indica en el
mensaje de conexión (`Conexión exitosa (sqlite)`).

## Notas de diseño

- **Librerías de conexión:** `sqlite3` (biblioteca estándar de Python) y
  `mysql-connector-python` (conector oficial de MySQL).
- **Credenciales fuera del código:** se leen desde `.env` con `python-dotenv`;
  `.env` no se versiona.
- **Consultas parametrizadas** en el DAO para evitar inyección SQL.
- **Relación "Consulta"** (Proyecto–Departamento, 1 a 1) del diagrama original:
  no se implementó por decisión del equipo.

## Integrantes

- Jean Yauri
- Joaquin