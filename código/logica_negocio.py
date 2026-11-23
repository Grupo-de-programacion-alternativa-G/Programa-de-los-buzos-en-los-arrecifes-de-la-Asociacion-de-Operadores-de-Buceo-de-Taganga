from datetime import date, timedelta
from math import sqrt
from random import randint

USO_MODERADO_MIN = 40
USO_ALTO_MIN = 70
USO_SATURACION_MIN = 90

NIVEL_BAJO = "Bajo"
NIVEL_MODERADO = "Moderado"
NIVEL_ALTO = "Alto"
NIVEL_SATURACION = "Saturación"


class Arrecife:
    def __init__(self, nombre: str, cupo_diario: int, fecha_inicio: date):
        self.nombre = nombre
        self.cupo_diario = cupo_diario
        self.fecha_inicio = fecha_inicio
        self.buzos_por_dia = []

    def validar_buzos(self, buzos: int):
        if buzos < 0 or buzos > self.cupo_diario:
            raise ValueError(f"Los buzos deben estar entre 0 y {self.cupo_diario}")

    def convertir_buzos(self, texto_buzos: str) -> int:
        try:
            buzos = int(texto_buzos)
        except ValueError:
            raise ValueError("Los buzos deben ser un número entero")
        self.validar_buzos(buzos)
        return buzos

    def convertir_dias_a_simular(self, texto_dias: str) -> int:
        try:
            dias = int(texto_dias)
        except ValueError:
            raise ValueError("El número de días debe ser un entero")
        if dias < 1:
            raise ValueError("Se debe simular al menos un día")
        return dias

    def agregar_buzos(self, buzos: int):
        self.validar_buzos(buzos)
        self.buzos_por_dia.append(buzos)

    def simular_dias(self, dias: int, minimo: int, maximo: int):
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo")
        for _ in range(dias):
            self.agregar_buzos(randint(minimo, maximo))

    def calcular_fecha_dia(self, indice: int) -> date:
        fecha_dia = self.fecha_inicio + timedelta(days=indice)
        return fecha_dia

    def calcular_fecha_siguiente(self) -> date:
        return self.calcular_fecha_dia(len(self.buzos_por_dia))

    def calcular_fecha_ultima(self) -> date | None:
        if len(self.buzos_por_dia) == 0:
            fecha_ultima = None
        else:
            fecha_ultima = self.calcular_fecha_dia(len(self.buzos_por_dia) - 1)
        return fecha_ultima

    def calcular_total_inmersiones(self) -> int:
        total_inmersiones = 0
        for buzos in self.buzos_por_dia:
            total_inmersiones = total_inmersiones + buzos
        return total_inmersiones

    def calcular_promedio_buzos(self) -> float | None:
        if len(self.buzos_por_dia) == 0:
            promedio_buzos = None
        else:
            promedio_buzos = self.calcular_total_inmersiones() / len(self.buzos_por_dia)
        return promedio_buzos

    def calcular_porcentaje_uso(self) -> float | None:
        if len(self.buzos_por_dia) == 0:
            porcentaje_uso = None
        else:
            capacidad_total = len(self.buzos_por_dia) * self.cupo_diario
            porcentaje_uso = (self.calcular_total_inmersiones() / capacidad_total) * 100
        return porcentaje_uso

    def calcular_desviacion_estandar(self) -> float | None:
        promedio_buzos = self.calcular_promedio_buzos()
        if promedio_buzos is None:
            desviacion_estandar = None
        else:
            suma_cuadrados = 0
            for buzos in self.buzos_por_dia:
                diferencia = buzos - promedio_buzos
                suma_cuadrados = suma_cuadrados + diferencia ** 2
            desviacion_estandar = sqrt(suma_cuadrados / len(self.buzos_por_dia))
        return desviacion_estandar

    def buscar_fecha_mas_buzos(self) -> date | None:
        if len(self.buzos_por_dia) == 0:
            fecha_mas_buzos = None
        else:
            mejor_indice = 0
            for indice in range(1, len(self.buzos_por_dia)):
                if self.buzos_por_dia[indice] > self.buzos_por_dia[mejor_indice]:
                    mejor_indice = indice
            fecha_mas_buzos = self.calcular_fecha_dia(mejor_indice)
        return fecha_mas_buzos

    def buscar_fecha_menos_buzos(self) -> date | None:
        if len(self.buzos_por_dia) == 0:
            fecha_menos_buzos = None
        else:
            peor_indice = 0
            for indice in range(1, len(self.buzos_por_dia)):
                if self.buzos_por_dia[indice] < self.buzos_por_dia[peor_indice]:
                    peor_indice = indice
            fecha_menos_buzos = self.calcular_fecha_dia(peor_indice)
        return fecha_menos_buzos

    def clasificar_dia(self, buzos: int) -> str:
        if buzos * 100 < USO_MODERADO_MIN * self.cupo_diario:
            nivel = NIVEL_BAJO
        elif buzos * 100 < USO_ALTO_MIN * self.cupo_diario:
            nivel = NIVEL_MODERADO
        elif buzos * 100 < USO_SATURACION_MIN * self.cupo_diario:
            nivel = NIVEL_ALTO
        else:
            nivel = NIVEL_SATURACION
        return nivel

    def contar_dias_por_nivel(self) -> list:
        dias_bajos = 0
        dias_moderados = 0
        dias_altos = 0
        dias_saturacion = 0
        for buzos in self.buzos_por_dia:
            nivel = self.clasificar_dia(buzos)
            if nivel == NIVEL_BAJO:
                dias_bajos = dias_bajos + 1
            elif nivel == NIVEL_MODERADO:
                dias_moderados = dias_moderados + 1
            elif nivel == NIVEL_ALTO:
                dias_altos = dias_altos + 1
            else:
                dias_saturacion = dias_saturacion + 1
        return [dias_bajos, dias_moderados, dias_altos, dias_saturacion]

    def buscar_indice_inicio_racha_saturacion_mas_larga(self) -> int | None:
        mejor_indice_inicio = None
        mejor_longitud = 0
        indice_inicio_actual = 0
        longitud_actual = 0
        for indice in range(len(self.buzos_por_dia)):
            if self.clasificar_dia(self.buzos_por_dia[indice]) == NIVEL_SATURACION:
                if longitud_actual == 0:
                    indice_inicio_actual = indice
                longitud_actual = longitud_actual + 1
                if longitud_actual > mejor_longitud:
                    mejor_longitud = longitud_actual
                    mejor_indice_inicio = indice_inicio_actual
            else:
                longitud_actual = 0
        return mejor_indice_inicio

    def calcular_racha_saturacion_mas_larga(self) -> int:
        indice_inicio = self.buscar_indice_inicio_racha_saturacion_mas_larga()
        longitud_racha = 0
        if indice_inicio is not None:
            indice = indice_inicio
            while (indice < len(self.buzos_por_dia)
                   and self.clasificar_dia(self.buzos_por_dia[indice]) == NIVEL_SATURACION):
                longitud_racha = longitud_racha + 1
                indice = indice + 1
        return longitud_racha

    def buscar_fecha_inicio_racha_saturacion_mas_larga(self) -> date | None:
        indice_inicio = self.buscar_indice_inicio_racha_saturacion_mas_larga()
        if indice_inicio is None:
            fecha_inicio_racha = None
        else:
            fecha_inicio_racha = self.calcular_fecha_dia(indice_inicio)
        return fecha_inicio_racha

    def calcular_dias_pendientes(self, fecha_referencia: date) -> int:
        dias_pendientes = (fecha_referencia - self.calcular_fecha_siguiente()).days
        if dias_pendientes < 0:
            dias_pendientes = 0
        return dias_pendientes


class Asociacion:
    def __init__(self):
        self.arrecifes = []

    def buscar_arrecife(self, nombre: str) -> Arrecife | None:
        nombre_limpio = nombre.strip()
        arrecife_encontrado = None
        for arrecife in self.arrecifes:
            if arrecife.nombre == nombre_limpio and arrecife_encontrado is None:
                arrecife_encontrado = arrecife
        return arrecife_encontrado

    def crear_arrecife(self,
                       nombre: str,
                       texto_cupo_diario: str,
                       texto_anio: str,
                       texto_mes: str,
                       texto_dia: str) -> Arrecife:
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            raise ValueError("El nombre no puede estar vacío")
        if self.buscar_arrecife(nombre_limpio) is not None:
            raise ValueError("Ya existe un arrecife con ese nombre")
        try:
            cupo_diario = int(texto_cupo_diario)
        except ValueError:
            raise ValueError("El cupo diario debe ser un número entero")
        if cupo_diario < 1:
            raise ValueError("El cupo diario debe ser al menos un buzo")
        try:
            fecha_inicio = date(int(texto_anio), int(texto_mes), int(texto_dia))
        except (ValueError, OverflowError):
            raise ValueError("La fecha no es válida")
        arrecife = Arrecife(nombre_limpio, cupo_diario, fecha_inicio)
        self.arrecifes.append(arrecife)
        return arrecife

    def buscar_arrecife_mayor_uso(self) -> Arrecife | None:
        arrecife_mayor = None
        uso_mayor = 0.0
        for arrecife in self.arrecifes:
            uso = arrecife.calcular_porcentaje_uso()
            if uso is not None:
                if arrecife_mayor is None or uso > uso_mayor:
                    arrecife_mayor = arrecife
                    uso_mayor = uso
        return arrecife_mayor

    def buscar_arrecife_menor_uso(self) -> Arrecife | None:
        arrecife_menor = None
        uso_menor = 0.0
        for arrecife in self.arrecifes:
            uso = arrecife.calcular_porcentaje_uso()
            if uso is not None:
                if arrecife_menor is None or uso < uso_menor:
                    arrecife_menor = arrecife
                    uso_menor = uso
        return arrecife_menor

    def cargar_linea_arrecife(self, linea: str):
        campos = linea.split(";")
        if len(campos) != 5:
            raise ValueError("La línea debe tener cinco campos")
        self.crear_arrecife(campos[0], campos[1], campos[2], campos[3], campos[4])

    def cargar_linea_buzos(self, linea: str):
        campos = linea.split(";")
        if len(campos) != 2:
            raise ValueError("La línea debe tener dos campos")
        arrecife = self.buscar_arrecife(campos[0])
        if arrecife is None:
            raise ValueError("No existe un arrecife con ese nombre")
        buzos = arrecife.convertir_buzos(campos[1])
        arrecife.agregar_buzos(buzos)
