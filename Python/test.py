import pSerie
import time
import numpy as np
import bDatos
#import matplotlib.pyplot as plt
import analisis

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

def ejemplo_db():

    db = bDatos.BDatos()
    db.reinicializar_db()
    """
    rng = np.random.default_rng()
    dL1_size = 100
    dL2_size = 10
    array_dL1 = rng.standard_normal(dL1_size) + 10  # dist normal alrededor de 10
    array_dL2 = rng.standard_normal(dL2_size)       # dist normal alrededor de 0
    array_timestamp_dL1 = []
    array_timestamp_dL2 = []
    for i in range(dL1_size):
        # Array dL1 tomado en el rango '1900-01-01 00:00:0' a '1999-01-01 00:00:00'
        array_timestamp_dL1.append(('%s-%s-%s %s:%s:%s' %(str(1900+i),'01','01','00','00','00')))    #'YYYY-MM-DD HH:MM:SS'
    for i in range(dL2_size):
        # Array dL1 tomado en el rango '2020-09-21 10:15:0' a '2020-09-21 10:15:09'
        array_timestamp_dL2.append(('%s-%s-%s %s:%s:%s' %('2020','09','21','10','15','0'+str(i))))    #'YYYY-MM-DD HH:MM:SS'
    db.add_n_datos(array_dL1, array_timestamp_dL1, 1)
    db.add_n_datos(array_dL2, array_timestamp_dL2, 2)
    """
    #lista = db.get_ultimo_mes(1)
    lista = db.get_ultima_semana(2)
    valor = []
    timestamp = []
    #print(lista)
    for i in range(len(lista)):
        print('i:',i)
        #for j in range(len(lista[0])):
        valor.append(lista[i][0])
        timestamp.append(lista[i][1])
    #print(valor)
    #print(timestamp)
    plt.plot(timestamp, valor)
    plt.show()
    """
    db.cur.execute('SELECT valor FROM Datos WHERE timestamp BETWEEN datetime("1900-01-01 00:00:00") AND datetime("1999-01-01 00:00:00")')
    resultados =[]
    for fila in db.cur.fetchall():
        resultados.append(fila)
    #print(resultados)
    promedio = 0
    for i in range(len(resultados)):
        promedio += resultados[i][0]
    promedio /= len(resultados)
    print(promedio)
    #db.cur.execute('SELECT date(?);', ('now',))
    #print(db.cur.fetchone())
    #print(timestamp)
    """
#test_db_init()
#add_datos()
#ejemplo_db()

 





def prueba(arg):
    if arg == '1':
        print('Exito')
    else:
        print('fail')
