# src/configurar_remoto.py
"""Deja MariaDB (XAMPP / phpMyAdmin) listo para conectarse desde otra PC o red.

Se ejecuta UNA vez, en la PC que tiene MariaDB:   python src/configurar_remoto.py
Crea la base y un usuario propio (no root) con permiso solo sobre esa base,
y al final imprime el bloque .env que debes copiar en las otras PC.
"""
import getpass
import platform
import re
import secrets
import shutil
import socket
import subprocess

import mysql.connector

NOMBRE_VALIDO = re.compile(r"[A-Za-z0-9_]+")


def preguntar(texto, defecto):
    valor = input(f"{texto} [{defecto}]: ").strip()
    return valor or defecto


def pedir_nombre(texto, defecto):
    while True:
        valor = preguntar(texto, defecto)
        if NOMBRE_VALIDO.fullmatch(valor):
            return valor
        print("  Solo letras, números y guion bajo.")


def si(texto):
    return input(f"{texto} (s/n): ").strip().lower() in ("s", "si", "sí")


def ip_tailscale():
    ejecutable = shutil.which("tailscale") or r"C:\Program Files\Tailscale\tailscale.exe"
    try:
        salida = subprocess.run([ejecutable, "ip", "-4"], capture_output=True, text=True, timeout=5)
        return salida.stdout.strip().splitlines()[0] if salida.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def ip_red_local():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # UDP: no envía nada, solo elige la interfaz
            return s.getsockname()[0]
    except OSError:
        return None


def abrir_firewall_windows(puerto, solo_tailscale):
    comando = ["netsh", "advfirewall", "firewall", "add", "rule", "name=EcoTech MariaDB",
               "dir=in", "action=allow", "protocol=TCP", f"localport={puerto}"]
    if solo_tailscale:
        comando.append("remoteip=100.64.0.0/10")
    if subprocess.run(comando, capture_output=True, text=True).returncode == 0:
        print("  Regla de firewall creada.")
    else:
        print("  No se pudo crear la regla. Abre CMD como Administrador y ejecuta:")
        print("  " + " ".join(f'"{c}"' if " " in c else c for c in comando))


def texto(valor):
    return valor.decode() if isinstance(valor, (bytes, bytearray)) else str(valor)


def main():
    print("=== Preparar MariaDB para acceso remoto (EcoTech) ===")
    puerto = int(preguntar("Puerto de MariaDB", "3306"))
    clave_root = getpass.getpass("Contraseña de root (XAMPP: Enter si está vacía): ")
    base = pedir_nombre("Nombre de la base", "ecotech")
    usuario = pedir_nombre("Usuario de la aplicación", "ecotech_app")
    clave = secrets.token_urlsafe(16)  # solo letras, números, '-' y '_': seguro dentro del SQL

    try:
        conexion = mysql.connector.connect(host="127.0.0.1", port=puerto, user="root",
                                           password=clave_root, connection_timeout=10)
    except mysql.connector.Error as error:
        raise SystemExit(f"No pude entrar como root: {error}\n¿Está iniciado MySQL en XAMPP?")

    cursor = conexion.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{base}` CHARACTER SET utf8mb4")
    # '%' = desde cualquier PC; 'localhost' evita que un usuario anónimo de XAMPP lo tape
    for origen in ("%", "localhost"):
        cuenta = f"'{usuario}'@'{origen}'"
        cursor.execute(f"CREATE USER IF NOT EXISTS {cuenta} IDENTIFIED BY '{clave}'")
        cursor.execute(f"ALTER USER {cuenta} IDENTIFIED BY '{clave}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON `{base}`.* TO {cuenta}")
    cursor.execute("FLUSH PRIVILEGES")
    conexion.commit()
    cursor.execute("SHOW VARIABLES WHERE Variable_name IN ('bind_address', 'skip_networking')")
    variables = {texto(k): texto(v) for k, v in cursor.fetchall()}
    conexion.close()
    print(f"\nListo: base '{base}' y usuario '{usuario}' creados (solo con permiso sobre esa base).")

    if variables.get("skip_networking") == "ON" or variables.get("bind_address") in ("127.0.0.1", "localhost", "::1"):
        print("AVISO: MariaDB solo escucha en esta PC. En XAMPP edita my.ini:")
        print("  quita 'skip-networking' y pon 'bind-address=0.0.0.0' bajo [mysqld]; reinicia MySQL.")

    tailscale, lan = ip_tailscale(), ip_red_local()
    if platform.system() == "Windows" and si("¿Abrir el puerto en el Firewall de Windows?"):
        solo_ts = bool(tailscale) and si("¿Permitir SOLO por Tailscale (más seguro)?")
        abrir_firewall_windows(puerto, solo_ts)

    host = tailscale or lan or "IP_DE_ESTA_PC"
    print("\nCopia esto en el archivo .env de las OTRAS PC (no lo subas a Git):\n")
    print("DB_ENGINE=mariadb")
    print(f"DB_HOST={host}")
    print(f"DB_PORT={puerto}")
    print(f"DB_NAME={base}")
    print(f"DB_USER={usuario}")
    print(f"DB_PASSWORD={clave}")
    print("DB_TIMEOUT=10\n")
    if not tailscale:
        print(f"Esa IP ({host}) solo sirve dentro de la misma red. Para otra red/lugar instala Tailscale")
        print("en ambas PC, vuelve a ejecutar este script y usará la IP 100.x.y.z.")
    print("Prueba desde la otra PC con:  python src/diagnostico.py")


if __name__ == "__main__":
    main()