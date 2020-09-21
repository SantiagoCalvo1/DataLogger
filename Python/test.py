import pSerie
import time
import numpy as np
import bDatos

######### TESTs DEL PUERTO SERIE #########
def test_echo():
    puerto = pSerie.PSerie()
    time.sleep(0.5)
    check(puerto.start_ADC(), True)
    time.sleep(0.5)
    check(puerto.configurar_micro(), True)
    time.sleep(0.5)
    check(puerto.micro_en_espera(), True)

def check(obtenido, esperado):
    if obtenido == esperado:
        print('Éxito!')
    else:
        print('Falla')

def test_recibir_buffer():
    puerto = pSerie.PSerie()
    check(puerto.start_ADC(), True)
    time.sleep(5)
    rx_array = np.zeros(10)
    check(puerto.recibir_datos(rx_array), True)
    print(rx_array)
    check(puerto.start_ADC(), True)
    time.sleep(11)
    rx_array = np.zeros(10)
    check(puerto.recibir_datos(rx_array), True)
    print(rx_array)

#test_echo()
#test_recibir_buffer()

##########################################

######### TESTs DE BASE DE DATOS #########
def test_db_init():
    db = bDatos.BDatos()
    db.reinicializar_db()

def add_datos():
    puerto = pSerie.PSerie()
    check(puerto.start_ADC(), True)
    time.sleep(5)
    rx_array = np.zeros(10)
    check(puerto.recibir_datos(rx_array), True)
    print(rx_array)
    print('bDatos<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    db = bDatos.BDatos()
    check(db.add_n_datos(rx_array, 1), True)
    db.cur.execute('SELECT * FROM Datos')
    for fila in db.cur.fetchall():
        print(fila)


#test_db_init()
add_datos()