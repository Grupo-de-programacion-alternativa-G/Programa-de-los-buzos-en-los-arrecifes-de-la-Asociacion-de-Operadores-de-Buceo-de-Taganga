from datetime import date
from os import system

from logica_negocio import Asociacion

MENSAJE_SIN_ARRECIFE = "No existe un arrecife con ese nombre"

objeto_asociacion = Asociacion()

system("cls")
print("=====================================")
print("Bienvenido al programa de buceo en arrecifes")
print("=====================================")

opcion = ""
while opcion != "7":
    print("=====================================")
    print("Menú")
    print("=====================================")
    print("1. Crear un arrecife")
    print("2. Registrar los buzos del siguiente día")
    print("3. Simular días")
    print("4. Mostrar el reporte de un arrecife")
    print("5. Mostrar los arrecifes de mayor y menor uso")
    print("6. Cargar los arrecifes y los buzos desde archivos")
    print("7. Salir")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        nombre_arrecife = input("Nombre del arrecife: ")
        texto_cupo_diario = input("Cupo diario: ")
        texto_anio_inicio = input("Año de inicio: ")
        texto_mes_inicio = input("Mes de inicio: ")
        texto_dia_inicio = input("Día de inicio: ")
        try:
            objeto_asociacion.crear_arrecife(nombre_arrecife, texto_cupo_diario,
                                             texto_anio_inicio, texto_mes_inicio,
                                             texto_dia_inicio)
            print("Arrecife creado")
        except ValueError as error:
            print(error)

    elif opcion == "2":
        nombre_arrecife = input("Nombre del arrecife: ")
        objeto_arrecife = objeto_asociacion.buscar_arrecife(nombre_arrecife)
        if objeto_arrecife is None:
            print(MENSAJE_SIN_ARRECIFE)
        else:
            fecha_siguiente = objeto_arrecife.calcular_fecha_siguiente()
            buzos_guardados = False
            while not buzos_guardados:
                try:
                    buzos = objeto_arrecife.convertir_buzos(input(f"Buzos del {fecha_siguiente}: "))
                    objeto_arrecife.agregar_buzos(buzos)
                    buzos_guardados = True
                except ValueError as error:
                    print(error)
            print("Día registrado")

    elif opcion == "3":
        nombre_arrecife = input("Nombre del arrecife: ")
        objeto_arrecife = objeto_asociacion.buscar_arrecife(nombre_arrecife)
        if objeto_arrecife is None:
            print(MENSAJE_SIN_ARRECIFE)
        else:
            try:
                dias_a_simular = objeto_arrecife.convertir_dias_a_simular(input("Días a simular: "))
                buzos_minimos = objeto_arrecife.convertir_buzos(input("Buzos mínimos: "))
                buzos_maximos = objeto_arrecife.convertir_buzos(input("Buzos máximos: "))
                objeto_arrecife.simular_dias(dias_a_simular, buzos_minimos, buzos_maximos)
                print(f"{dias_a_simular} días simulados")
            except ValueError as error:
                print(error)

    elif opcion == "4":
        nombre_arrecife = input("Nombre del arrecife: ")
        objeto_arrecife = objeto_asociacion.buscar_arrecife(nombre_arrecife)
        if objeto_arrecife is None:
            print(MENSAJE_SIN_ARRECIFE)
        else:
            print("=====================================")
            print("Reporte del arrecife")
            print("=====================================")
            print(f"Arrecife: {objeto_arrecife.nombre}")
            print(f"Cupo diario: {objeto_arrecife.cupo_diario}")
            dias_registrados = len(objeto_arrecife.buzos_por_dia)
            if dias_registrados == 0:
                print("El arrecife no tiene días registrados")
            else:
                total_inmersiones = objeto_arrecife.calcular_total_inmersiones()
                promedio_buzos = objeto_arrecife.calcular_promedio_buzos()
                porcentaje_uso = objeto_arrecife.calcular_porcentaje_uso()
                desviacion_estandar = objeto_arrecife.calcular_desviacion_estandar()
                fecha_mas_buzos = objeto_arrecife.buscar_fecha_mas_buzos()
                fecha_menos_buzos = objeto_arrecife.buscar_fecha_menos_buzos()
                dias_por_nivel = objeto_arrecife.contar_dias_por_nivel()
                racha_mas_larga = objeto_arrecife.calcular_racha_saturacion_mas_larga()
                fecha_inicio_racha = objeto_arrecife.buscar_fecha_inicio_racha_saturacion_mas_larga()
                fecha_ultima = objeto_arrecife.calcular_fecha_ultima()
                dias_pendientes = objeto_arrecife.calcular_dias_pendientes(date.today())

                print(f"Días registrados: {dias_registrados}")
                print(f"Total de inmersiones: {total_inmersiones}")
                print(f"Promedio de buzos por día: {round(promedio_buzos, 2)}")
                print(f"Porcentaje de uso: {round(porcentaje_uso, 2)} %")
                print(f"Desviación estándar: {round(desviacion_estandar, 2)}")
                print(f"Día con más buzos: {fecha_mas_buzos}")
                print(f"Día con menos buzos: {fecha_menos_buzos}")
                print(f"Días en uso bajo: {dias_por_nivel[0]}")
                print(f"Días en uso moderado: {dias_por_nivel[1]}")
                print(f"Días en uso alto: {dias_por_nivel[2]}")
                print(f"Días en saturación: {dias_por_nivel[3]}")
                if fecha_inicio_racha is None:
                    print("El arrecife no tuvo días en saturación")
                else:
                    print(f"Racha de saturación más larga: {racha_mas_larga} días, desde el {fecha_inicio_racha}")
                print(f"Último día registrado: {fecha_ultima}")
                if dias_pendientes == 0:
                    print("El registro está al día")
                else:
                    print(f"Días pendientes por registrar: {dias_pendientes}")

    elif opcion == "5":
        arrecife_mayor_uso = objeto_asociacion.buscar_arrecife_mayor_uso()
        arrecife_menor_uso = objeto_asociacion.buscar_arrecife_menor_uso()
        if arrecife_mayor_uso is None or arrecife_menor_uso is None:
            print("Ningún arrecife tiene días registrados")
        else:
            uso_mayor = arrecife_mayor_uso.calcular_porcentaje_uso()
            uso_menor = arrecife_menor_uso.calcular_porcentaje_uso()
            print(f"Mayor uso: {arrecife_mayor_uso.nombre}, {round(uso_mayor, 2)} %")
            print(f"Menor uso: {arrecife_menor_uso.nombre}, {round(uso_menor, 2)} %")

    elif opcion == "6":
        if len(objeto_asociacion.arrecifes) > 0:
            print("La carga solo se puede hacer con el programa sin arrecifes")
        else:
            ruta_arrecifes = input("Ruta del archivo de arrecifes: ")
            try:
                archivo_arrecifes = open(ruta_arrecifes, encoding="utf-8")
                lineas_arrecifes = archivo_arrecifes.readlines()
                archivo_arrecifes.close()
                archivo_arrecifes_existe = True
            except OSError:
                archivo_arrecifes_existe = False
                print("El archivo no existe")

            if archivo_arrecifes_existe:
                arrecifes_cargados = 0
                for indice in range(1, len(lineas_arrecifes)):
                    if lineas_arrecifes[indice].strip() != "":
                        try:
                            objeto_asociacion.cargar_linea_arrecife(lineas_arrecifes[indice])
                            arrecifes_cargados = arrecifes_cargados + 1
                        except ValueError as error:
                            print(f"Línea {indice + 1} descartada: {error}")
                print(f"Arrecifes cargados: {arrecifes_cargados}")

                ruta_buzos = input("Ruta del archivo de buzos: ")
                try:
                    archivo_buzos = open(ruta_buzos, encoding="utf-8")
                    lineas_buzos = archivo_buzos.readlines()
                    archivo_buzos.close()
                    archivo_buzos_existe = True
                except OSError:
                    archivo_buzos_existe = False
                    print("El archivo no existe")

                if archivo_buzos_existe:
                    dias_cargados = 0
                    for indice in range(1, len(lineas_buzos)):
                        if lineas_buzos[indice].strip() != "":
                            try:
                                objeto_asociacion.cargar_linea_buzos(lineas_buzos[indice])
                                dias_cargados = dias_cargados + 1
                            except ValueError as error:
                                print(f"Línea {indice + 1} descartada: {error}")
                    print(f"Días cargados: {dias_cargados}")

    elif opcion != "7":
        print("La opción no es válida")
