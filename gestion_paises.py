"""
=============================================================
TPI - Gestión de Datos de Países en Python
Programación 1
=============================================================
Descripción: Sistema de gestión de información de países con
menú interactivo. Permite agregar, actualizar, buscar, filtrar,
ordenar y obtener estadísticas sobre países del mundo.
=============================================================
"""

import csv
import os

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
ARCHIVO_CSV = "paises.csv"
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]
CONTINENTES_VALIDOS = ["América", "Europa", "Asia", "África", "Oceanía", "Antártida"]


# ═════════════════════════════════════════════
# MÓDULO 1: LECTURA Y ESCRITURA DE ARCHIVOS
# ═════════════════════════════════════════════

def cargar_paises():
    """
    Lee el archivo CSV y retorna una lista de diccionarios.
    Cada diccionario representa un país con sus datos.
    Retorna lista vacía si el archivo no existe o tiene errores.
    """
    paises = []

    if not os.path.exists(ARCHIVO_CSV):
        print(f"[AVISO] No se encontró '{ARCHIVO_CSV}'. Se iniciará con lista vacía.")
        return paises

    try:
        with open(ARCHIVO_CSV, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Validar que el CSV tenga los campos esperados
            if lector.fieldnames is None or not all(c in lector.fieldnames for c in CAMPOS):
                print("[ERROR] El archivo CSV no tiene el formato correcto.")
                print(f"        Campos esperados: {CAMPOS}")
                return paises

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    pais = {
                        "nombre":      fila["nombre"].strip(),
                        "poblacion":   int(fila["poblacion"].strip()),
                        "superficie":  int(fila["superficie"].strip()),
                        "continente":  fila["continente"].strip()
                    }
                    # Validar que no haya campos vacíos
                    if not all(str(v) for v in pais.values()):
                        print(f"[AVISO] Fila {numero_fila} omitida: tiene campos vacíos.")
                        continue
                    paises.append(pais)

                except ValueError:
                    print(f"[AVISO] Fila {numero_fila} omitida: población o superficie no son números válidos.")
                    continue

    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo: {e}")

    return paises


def guardar_paises(paises):
    """
    Guarda la lista de países en el archivo CSV.
    Sobreescribe el archivo con los datos actuales.
    """
    try:
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
        print("[OK] Datos guardados correctamente en el archivo CSV.")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo: {e}")


# ═════════════════════════════════════════════
# MÓDULO 2: ALTA Y MODIFICACIÓN
# ═════════════════════════════════════════════

def agregar_pais(paises):
    """
    Solicita al usuario los datos de un nuevo país y lo agrega
    a la lista si no existe previamente (sin campos vacíos).
    """
    print("\n─── Agregar nuevo país ───")

    # Nombre
    nombre = input("  Nombre del país: ").strip()
    if not nombre:
        print("[ERROR] El nombre no puede estar vacío.")
        return

    # Verificar duplicado
    if buscar_por_nombre_exacto(paises, nombre) is not None:
        print(f"[ERROR] Ya existe un país con el nombre '{nombre}'.")
        return

    # Población
    poblacion = pedir_entero_positivo("  Población: ")
    if poblacion is None:
        return

    # Superficie
    superficie = pedir_entero_positivo("  Superficie en km²: ")
    if superficie is None:
        return

    # Continente
    continente = pedir_continente()
    if continente is None:
        return

    # Crear y agregar
    nuevo_pais = {
        "nombre":     nombre,
        "poblacion":  poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo_pais)
    guardar_paises(paises)
    print(f"[OK] País '{nombre}' agregado exitosamente.")


def actualizar_pais(paises):
    """
    Busca un país por nombre exacto y permite actualizar
    su población y/o superficie.
    """
    print("\n─── Actualizar país ───")
    nombre = input("  Nombre del país a actualizar: ").strip()

    pais = buscar_por_nombre_exacto(paises, nombre)
    if pais is None:
        print(f"[ERROR] No se encontró ningún país con el nombre '{nombre}'.")
        return

    print(f"\n  Datos actuales de {pais['nombre']}:")
    print(f"    Población:  {pais['poblacion']:,}")
    print(f"    Superficie: {pais['superficie']:,} km²")
    print()

    # Nueva población
    entrada = input("  Nueva población (Enter para mantener actual): ").strip()
    if entrada:
        try:
            nueva_poblacion = int(entrada)
            if nueva_poblacion <= 0:
                print("[ERROR] La población debe ser un número positivo.")
                return
            pais["poblacion"] = nueva_poblacion
        except ValueError:
            print("[ERROR] Valor inválido para población.")
            return

    # Nueva superficie
    entrada = input("  Nueva superficie en km² (Enter para mantener actual): ").strip()
    if entrada:
        try:
            nueva_superficie = int(entrada)
            if nueva_superficie <= 0:
                print("[ERROR] La superficie debe ser un número positivo.")
                return
            pais["superficie"] = nueva_superficie
        except ValueError:
            print("[ERROR] Valor inválido para superficie.")
            return

    guardar_paises(paises)
    print(f"[OK] País '{pais['nombre']}' actualizado correctamente.")


# ═════════════════════════════════════════════
# MÓDULO 3: BÚSQUEDA Y FILTROS
# ═════════════════════════════════════════════

def buscar_pais(paises):
    """
    Busca países cuyo nombre contenga el texto ingresado
    (búsqueda parcial, sin distinguir mayúsculas).
    """
    print("\n─── Buscar país ───")
    termino = input("  Ingresá el nombre (parcial o completo): ").strip()

    if not termino:
        print("[ERROR] El término de búsqueda no puede estar vacío.")
        return

    resultados = [
        p for p in paises
        if termino.lower() in p["nombre"].lower()
    ]

    if not resultados:
        print(f"[INFO] No se encontraron países que contengan '{termino}'.")
    else:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        mostrar_tabla(resultados)


def filtrar_por_continente(paises):
    """
    Filtra y muestra los países que pertenecen al continente ingresado.
    """
    print("\n─── Filtrar por continente ───")
    continente = pedir_continente()
    if continente is None:
        return

    resultados = [p for p in paises if p["continente"].lower() == continente.lower()]

    if not resultados:
        print(f"[INFO] No hay países registrados en '{continente}'.")
    else:
        print(f"\n  Países en {continente} ({len(resultados)}):")
        mostrar_tabla(resultados)


def filtrar_por_poblacion(paises):
    """
    Filtra países dentro de un rango de población definido por el usuario.
    """
    print("\n─── Filtrar por rango de población ───")

    minimo = pedir_entero_positivo("  Población mínima: ")
    if minimo is None:
        return

    maximo = pedir_entero_positivo("  Población máxima: ")
    if maximo is None:
        return

    if minimo > maximo:
        print("[ERROR] La población mínima no puede ser mayor que la máxima.")
        return

    resultados = [
        p for p in paises
        if minimo <= p["poblacion"] <= maximo
    ]

    if not resultados:
        print(f"[INFO] No hay países con población entre {minimo:,} y {maximo:,}.")
    else:
        print(f"\n  Países con población entre {minimo:,} y {maximo:,} ({len(resultados)}):")
        mostrar_tabla(resultados)


def filtrar_por_superficie(paises):
    """
    Filtra países dentro de un rango de superficie definido por el usuario.
    """
    print("\n─── Filtrar por rango de superficie ───")

    minimo = pedir_entero_positivo("  Superficie mínima (km²): ")
    if minimo is None:
        return

    maximo = pedir_entero_positivo("  Superficie máxima (km²): ")
    if maximo is None:
        return

    if minimo > maximo:
        print("[ERROR] La superficie mínima no puede ser mayor que la máxima.")
        return

    resultados = [
        p for p in paises
        if minimo <= p["superficie"] <= maximo
    ]

    if not resultados:
        print(f"[INFO] No hay países con superficie entre {minimo:,} y {maximo:,} km².")
    else:
        print(f"\n  Países con superficie entre {minimo:,} y {maximo:,} km² ({len(resultados)}):")
        mostrar_tabla(resultados)


# ═════════════════════════════════════════════
# MÓDULO 4: ORDENAMIENTO
# ═════════════════════════════════════════════

def ordenar_paises(paises):
    """
    Muestra el menú de ordenamiento y ordena la lista según la
    opción elegida (nombre, población o superficie) en forma
    ascendente o descendente.
    """
    if not paises:
        print("[INFO] No hay países para ordenar.")
        return

    print("\n─── Ordenar países ───")
    print("  ¿Por qué campo?")
    print("   1. Nombre")
    print("   2. Población")
    print("   3. Superficie")

    campo_opcion = input("  Opción: ").strip()
    campos_map = {"1": "nombre", "2": "poblacion", "3": "superficie"}

    if campo_opcion not in campos_map:
        print("[ERROR] Opción inválida.")
        return

    campo = campos_map[campo_opcion]

    print("\n  ¿En qué orden?")
    print("   1. Ascendente")
    print("   2. Descendente")
    orden_opcion = input("  Opción: ").strip()

    if orden_opcion not in ("1", "2"):
        print("[ERROR] Opción inválida.")
        return

    descendente = (orden_opcion == "2")

    # Ordenamiento con sorted() usando función lambda como clave
    if campo == "nombre":
        resultado = sorted(paises, key=lambda p: p["nombre"].lower(), reverse=descendente)
    else:
        resultado = sorted(paises, key=lambda p: p[campo], reverse=descendente)

    orden_texto = "descendente" if descendente else "ascendente"
    print(f"\n  Países ordenados por {campo} ({orden_texto}):")
    mostrar_tabla(resultado)


# ═════════════════════════════════════════════
# MÓDULO 5: ESTADÍSTICAS
# ═════════════════════════════════════════════

def mostrar_estadisticas(paises):
    """
    Calcula y muestra estadísticas generales del dataset:
    - País con mayor y menor población
    - Promedio de población
    - Promedio de superficie
    - Cantidad de países por continente
    """
    if not paises:
        print("[INFO] No hay datos para calcular estadísticas.")
        return

    print("\n─────────────────────────────────────────────")
    print("             ESTADÍSTICAS GENERALES          ")
    print("─────────────────────────────────────────────")

    # País con mayor y menor población
    mayor_pob = max(paises, key=lambda p: p["poblacion"])
    menor_pob = min(paises, key=lambda p: p["poblacion"])

    print(f"\n  Población:")
    print(f"    Mayor: {mayor_pob['nombre']} ({mayor_pob['poblacion']:,} hab.)")
    print(f"    Menor: {menor_pob['nombre']} ({menor_pob['poblacion']:,} hab.)")

    # Promedio de población
    total_poblacion = sum(p["poblacion"] for p in paises)
    promedio_pob = total_poblacion // len(paises)
    print(f"    Promedio: {promedio_pob:,} hab.")

    # Promedio de superficie
    total_superficie = sum(p["superficie"] for p in paises)
    promedio_sup = total_superficie // len(paises)
    print(f"\n  Superficie:")
    print(f"    Promedio: {promedio_sup:,} km²")

    # Cantidad de países por continente
    print("\n  Países por continente:")
    conteo = contar_por_continente(paises)
    for continente, cantidad in sorted(conteo.items()):
        barra = "█" * cantidad
        print(f"    {continente:<15} {cantidad:>3}  {barra}")

    print(f"\n  Total de países en el sistema: {len(paises)}")
    print("─────────────────────────────────────────────")


def contar_por_continente(paises):
    """
    Retorna un diccionario con la cantidad de países por continente.
    Clave: nombre del continente. Valor: cantidad de países.
    """
    conteo = {}
    for pais in paises:
        continente = pais["continente"]
        if continente in conteo:
            conteo[continente] += 1
        else:
            conteo[continente] = 1
    return conteo


# ═════════════════════════════════════════════
# MÓDULO 6: UTILIDADES / HELPERS
# ═════════════════════════════════════════════

def buscar_por_nombre_exacto(paises, nombre):
    """
    Busca un país por nombre exacto (sin distinguir mayúsculas).
    Retorna el diccionario del país o None si no se encuentra.
    """
    nombre_lower = nombre.lower()
    for pais in paises:
        if pais["nombre"].lower() == nombre_lower:
            return pais
    return None


def pedir_entero_positivo(mensaje):
    """
    Solicita al usuario un número entero positivo.
    Retorna el número o None si el valor ingresado es inválido.
    """
    entrada = input(mensaje).strip()
    try:
        numero = int(entrada)
        if numero <= 0:
            print("[ERROR] El valor debe ser un número entero positivo.")
            return None
        return numero
    except ValueError:
        print(f"[ERROR] '{entrada}' no es un número entero válido.")
        return None


def pedir_continente():
    """
    Muestra los continentes disponibles y solicita al usuario
    que elija uno por número. Retorna el nombre del continente elegido.
    """
    print("  Continentes disponibles:")
    for i, cont in enumerate(CONTINENTES_VALIDOS, start=1):
        print(f"   {i}. {cont}")

    entrada = input("  Seleccioná el número del continente: ").strip()
    try:
        indice = int(entrada) - 1
        if 0 <= indice < len(CONTINENTES_VALIDOS):
            return CONTINENTES_VALIDOS[indice]
        else:
            print("[ERROR] Número fuera de rango.")
            return None
    except ValueError:
        print("[ERROR] Ingresá un número válido.")
        return None


def mostrar_tabla(paises):
    """
    Muestra una lista de países en formato de tabla alineada en consola.
    """
    if not paises:
        print("  (sin resultados)")
        return

    # Encabezado
    print()
    print(f"  {'NOMBRE':<30} {'POBLACIÓN':>15} {'SUPERFICIE (km²)':>18} {'CONTINENTE':<15}")
    print(f"  {'─'*30} {'─'*15} {'─'*18} {'─'*15}")

    for p in paises:
        print(
            f"  {p['nombre']:<30} "
            f"{p['poblacion']:>15,} "
            f"{p['superficie']:>18,} "
            f"{p['continente']:<15}"
        )
    print()


def mostrar_menu():
    """
    Imprime el menú principal del sistema en consola.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║      GESTIÓN DE DATOS DE PAÍSES          ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Agregar país                         ║")
    print("║  2. Actualizar país (población/superficie║")
    print("║  3. Buscar país por nombre               ║")
    print("║──────────────────────────────────────────║")
    print("║  FILTROS                                 ║")
    print("║  4. Filtrar por continente               ║")
    print("║  5. Filtrar por rango de población       ║")
    print("║  6. Filtrar por rango de superficie      ║")
    print("║──────────────────────────────────────────║")
    print("║  7. Ordenar países                       ║")
    print("║  8. Ver estadísticas                     ║")
    print("║  9. Ver todos los países                 ║")
    print("║──────────────────────────────────────────║")
    print("║  0. Salir                                ║")
    print("╚══════════════════════════════════════════╝")
    print("  Opción: ", end="")


# ═════════════════════════════════════════════
# PROGRAMA PRINCIPAL
# ═════════════════════════════════════════════

def main():
    """
    Función principal. Carga los datos, muestra el menú
    y delega en las funciones correspondientes según la
    opción elegida por el usuario.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║  Iniciando sistema de gestión de países  ║")
    print("╚══════════════════════════════════════════╝")

    # Cargar datos desde el CSV al iniciar
    paises = cargar_paises()
    print(f"  {len(paises)} países cargados desde '{ARCHIVO_CSV}'.")

    # Mapa de opciones → funciones
    opciones = {
        "1": lambda: agregar_pais(paises),
        "2": lambda: actualizar_pais(paises),
        "3": lambda: buscar_pais(paises),
        "4": lambda: filtrar_por_continente(paises),
        "5": lambda: filtrar_por_poblacion(paises),
        "6": lambda: filtrar_por_superficie(paises),
        "7": lambda: ordenar_paises(paises),
        "8": lambda: mostrar_estadisticas(paises),
        "9": lambda: mostrar_tabla(paises),
    }

    while True:
        mostrar_menu()
        opcion = input().strip()

        if opcion == "0":
            print("\n  ¡Hasta luego!\n")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("[ERROR] Opción inválida. Ingresá un número del 0 al 9.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
