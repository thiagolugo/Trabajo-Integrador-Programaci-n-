# 🌍 Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**

Sistema de consola desarrollado en Python que permite gestionar información sobre países del mundo: agregar, actualizar, buscar, filtrar, ordenar y obtener estadísticas a partir de un dataset en formato CSV.

---

## 📁 Estructura del proyecto

```
/
├── gestion_paises.py   # Código fuente principal
├── paises.csv          # Dataset base (54 países)
├── README.md           # Este archivo
└── informe.pdf         # Documentación académica
```

---

## ▶️ Cómo ejecutar el programa

**Requisitos:** Python 3.x instalado (sin dependencias externas).

```bash
# Clonar el repositorio
git clone https://github.com/USUARIO/REPOSITORIO.git
cd REPOSITORIO

# Ejecutar el programa
python3 gestion_paises.py
```

> En Windows reemplazar `python3` por `python`.

---

## 🗂️ Funcionalidades

| Opción | Función |
|--------|---------|
| 1 | Agregar un nuevo país |
| 2 | Actualizar población/superficie de un país |
| 3 | Buscar país por nombre (parcial o exacto) |
| 4 | Filtrar por continente |
| 5 | Filtrar por rango de población |
| 6 | Filtrar por rango de superficie |
| 7 | Ordenar por nombre, población o superficie (asc/desc) |
| 8 | Ver estadísticas generales |
| 9 | Ver todos los países |
| 0 | Salir |

---

## 📊 Formato del CSV

El archivo `paises.csv` utiliza el siguiente formato:

```
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
```

**Campos:**
- `nombre`: nombre del país (string)
- `poblacion`: cantidad de habitantes (entero positivo)
- `superficie`: superficie en km² (entero positivo)
- `continente`: uno de América, Europa, Asia, África, Oceanía, Antártida

---

## 💻 Ejemplos de uso

### Agregar un país
```
Opción: 1
─── Agregar nuevo país ───
  Nombre del país: Noruega
  Población: 5421241
  Superficie en km²: 323802
  Continentes disponibles:
   1. América
   2. Europa
   ...
  Seleccioná el número del continente: 2
[OK] País 'Noruega' agregado exitosamente.
```

### Buscar por nombre
```
Opción: 3
─── Buscar país ───
  Ingresá el nombre (parcial o completo): bra

  Se encontraron 1 resultado(s):
  NOMBRE                          POBLACIÓN   SUPERFICIE (km²) CONTINENTE
  ────────────────────────────── ─────────── ──────────────── ───────────────
  Brasil                         213,993,437        8,515,767 América
```

### Estadísticas
```
─────────────────────────────────────────────
             ESTADÍSTICAS GENERALES
─────────────────────────────────────────────
  Población:
    Mayor: China (1,444,216,107 hab.)
    Menor: Fiyi (902,906 hab.)
    Promedio: 119,309,584 hab.

  Superficie:
    Promedio: 1,877,869 km²

  Países por continente:
    América          14  ██████████████
    Asia             12  ████████████
    Europa           14  ██████████████
    Oceanía           4  ████
    África           10  ██████████

  Total de países en el sistema: 54
```

---

## 👥 Integrantes

| Nombre |  
|--------|
| Thiago Lugo |
| Lautaro Torres |

---

## 🎥 Video demostrativo

🔗 video de Lautaro Torres y Thiago Lugo: https://youtu.be/qnj67ThbZwM


## 📄 Documentación PDF

🔗 
