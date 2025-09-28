"""
C2005 - Algoritmos y Programación Básica (UVG)
Fase 2 – Prototipo funcional (consola, sin archivos, sin while True)

Idea alineada con Fase 1: agenda virtual + recordatorios + generador básico de tareas.
Estructura de datos: MATRIZ (lista de listas). Cada tarea es:
[id, titulo, fecha(YYYY-MM-DD), hora(HH:MM), prioridad{1=alta,2=media,3=baja}, estado{"pendiente"/"hecha"}]

NOTA IMPORTANTE PARA EL DOCENTE:
- No se usan archivos (persistencia) ni bucles while True.
- Todo está en funciones simples, con cadenas y listas (matriz) y un demo determinístico.
- El "recordatorio" se implementa como una verificación de tareas próximas en una ventana de tiempo.
"""

from datetime import datetime, timedelta
from typing import List, Tuple

Tarea = List[str]  # por simplicidad usaremos List[str] aunque algunas posiciones son números
Matriz = List[Tarea]

# --------------------------
# Utilidades simples
# --------------------------

def _dt(fecha_iso: str, hora_hm: str) -> datetime:
    """Convierte 'YYYY-MM-DD' y 'HH:MM' a datetime (sin zona). Lanza ValueError si hay formato inválido."""
    return datetime.strptime(f"{fecha_iso} {hora_hm}", "%Y-%m-%d %H:%M")

def _s(fecha: datetime) -> Tuple[str, str]:
    """Convierte datetime -> ('YYYY-MM-DD','HH:MM')"""
    return fecha.strftime("%Y-%m-%d"), fecha.strftime("%H:%M")

# --------------------------
# CRUD de tareas en MATRIZ
# --------------------------

def crear_tarea(matriz: Matriz, titulo: str, fecha_iso: str, hora_hm: str, prioridad: int) -> None:
    """
    Agrega una tarea a la matriz. 'prioridad' debe estar en {1,2,3}.
    Genera id incremental como cadena.
    Estado inicial: 'pendiente'.
    """
    if prioridad not in (1, 2, 3):
        raise ValueError("La prioridad debe ser 1 (alta), 2 (media) o 3 (baja).")
    # validación de fecha/hora
    _ = _dt(fecha_iso, hora_hm)
    nuevo_id = str(len(matriz) + 1)
    matriz.append([nuevo_id, titulo, fecha_iso, hora_hm, str(prioridad), "pendiente"])

def completar_tarea(matriz: Matriz, id_tarea: str) -> bool:
    """Marca una tarea como 'hecha'. Regresa True si la encontró, False en otro caso."""
    for fila in matriz:
        if fila[0] == id_tarea:
            fila[5] = "hecha"
            return True
    return False

def agenda_ordenada(matriz: Matriz) -> Matriz:
    """
    Devuelve una NUEVA lista ordenada por fecha/hora y prioridad (1 alta primero).
    No modifica la matriz original.
    """
    def clave(fila: Tarea):
        f, h, p = fila[2], fila[3], int(fila[4])
        return (_dt(f, h), p)
    return sorted([fila[:] for fila in matriz], key=clave)

def recordar_proximas(matriz: Matriz, ahora: datetime, ventana_min: int = 90) -> Matriz:
    """
    Devuelve lista de tareas PENDIENTES cuya hora esté dentro de [ahora, ahora+ventana].
    """
    limite = ahora + timedelta(minutes=ventana_min)
    proximas = []
    for fila in matriz:
        if fila[5] != "pendiente":
            continue
        f, h = fila[2], fila[3]
        cuando = _dt(f, h)
        if ahora <= cuando <= limite:
            proximas.append(fila[:])
    return agenda_ordenada(proximas)

def generar_tareas_automaticas(matriz: Matriz, fecha_base: str, hora_estudio: str, dias: int = 3) -> None:
    """
    Generador básico de tareas (muy simple) que crea 'Bloque de estudio' por 'dias'
    consecutivos a la misma hora, prioridad media (2).
    Sirve para demostrar la parte de 'generador de tareas' de la idea.
    """
    base = datetime.strptime(fecha_base, "%Y-%m-%d")
    for i in range(dias):
        fecha_i = base + timedelta(days=i)
        f_iso, _ = _s(fecha_i.replace(hour=0, minute=0))
        crear_tarea(matriz, "Bloque de estudio", f_iso, hora_estudio, 2)

# --------------------------
# Métricas simples (para mostrar valor)
# --------------------------

def metricas(matriz: Matriz) -> dict:
    total = len(matriz)
    hechas = sum(1 for f in matriz if f[5] == "hecha")
    pend = total - hechas
    pct = 0 if total == 0 else round(100 * hechas / total, 1)
    return {"total": total, "pendientes": pend, "hechas": hechas, "%_completadas": pct}

# --------------------------
# Impresión de resultados
# --------------------------

def imprimir_tabla(matriz: Matriz, titulo: str) -> None:
    print(f"\n== {titulo} ==")
    print("ID | Título                  | Fecha       | Hora  | Pri | Estado")
    print("---+--------------------------+-------------+-------+-----+--------")
    for fila in matriz:
        print(f"{fila[0]:>2} | {fila[1]:<24} | {fila[2]} | {fila[3]:<5} |  {fila[4]}  | {fila[5]}")

def demo() -> None:
    """
    Demostración determinística (sin input) para evaluar fácilmente el prototipo:
    1) Crea tareas típicas del "estudiante con empleo de medio tiempo".
    2) Genera automáticamente bloques de estudio próximos.
    3) Muestra agenda ordenada.
    4) Muestra recordatorios próximos (90 min desde 'ahora').
    5) Completa una tarea y muestra métricas.
    """
    matriz: Matriz = []

    # 1) Tareas del perfil (alineado a Fase 1)
    crear_tarea(matriz, "Clase Cálculo I",        "2025-10-02", "07:00", 1)
    crear_tarea(matriz, "Turno trabajo (tarde)",  "2025-10-02", "14:00", 2)
    crear_tarea(matriz, "Entrega reporte IM2020", "2025-10-02", "20:00", 1)
    crear_tarea(matriz, "Descanso/pausa activa",  "2025-10-02", "16:30", 3)

    # 2) Generador básico de tareas automáticas (3 días, misma hora)
    generar_tareas_automaticas(matriz, fecha_base="2025-10-02", hora_estudio="19:00", dias=3)

    # 3) Agenda ordenada
    imprimir_tabla(agenda_ordenada(matriz), "Agenda ordenada por fecha/hora y prioridad")

    # 4) Recordatorios próximos (supongamos que AHORA es 2025-10-02 13:00)
    ahora = datetime(2025, 10, 2, 13, 0)
    proximas = recordar_proximas(matriz, ahora=ahora, ventana_min=90)
    imprimir_tabla(proximas, "Recordatorios en los próximos 90 minutos")

    # 5) Completar una tarea y ver métricas
    completar_tarea(matriz, "3")  # marcar 'Entrega reporte IM2020' como hecha
    imprimir_tabla(matriz, "Estado tras completar una tarea")
    print("\nMétricas:", metricas(matriz))

if __name__ == "__main__":
    demo()
