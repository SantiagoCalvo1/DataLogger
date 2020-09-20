import dataLogger
import numpy as np
import time 

def inicializacion():
    try: dataL = dataLogger.DataLogger('nombre', 'descripción')
    except: 
        print('ERROR: En la inicialización')
        return False
    print(dataL)
    print(dataL.puerto)
    dataL.puerto.close()
    return True

def adquisicion():
    try: dataL = dataLogger.DataLogger('nombre', 'descripción')
    except: 
        print('ERROR: En la inicialización')
        dataL.puerto.close()
        return False
    array = np.zeros(512)
    try: array = dataL.recibir_datos(array)
    except: 
        print('ERROR: En la adquisición')
        dataL.puerto.close()
        return False
    if np.size(array) == 0:
        print('ERROR: En la adquisición. array = None')
        dataL.puerto.close()
        return False
    else:
        dataL.puerto.close()
        print(array)
        return True

def comunicacion():

    dataL = dataLogger.DataLogger('nombre', 'descripción')
    
    # Automatico comienza en NADA
    # Pasarlo a que ADQUIRIR datos. ADC -> Memoria
    if dataL.comenzar_adquisicion():
        print('Ha comenzado la adquisicion. 3 seg')
    
    # Pasarlo a ENVIAR_DATOS. Micro -> PC
    time.sleep(3)
    array = np.zeros(10)
    if dataL.recibir_datos(array):
        print(array)
        print('OK: El chequeo cuando no hay overflow')
    else: return print('ERROR: El chequeo cuando no hay overflow')
    
    if dataL.comenzar_adquisicion():
        print('Ha comenzado la adquisicion. 10 seg')
    time.sleep(10)
    if not dataL.recibir_datos(array):
        print(array)
        print('OK: El chequeo cuando si hay overflow')
    else: return print('ERROR: El chequeo cuando si hay overflow')
    
    time.sleep(2)
    # Pasarlo a NADA
    if dataL.cambiar_estado_a_nada():
        return print('OK: Cambio a NADA')
    else: return print('ERROR: Cambio a NADA')

"""
if inicializacion():
    print('Inicialización exitosa!')
"""
"""
if adquisicion():
    print('Adquisicón exitosa!')
"""
comunicacion() 
