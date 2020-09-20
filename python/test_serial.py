import puertoSerie
import time 
import numpy as np

def test_echo_ascii(char):
    try:    puerto = puertoSerie.PuertoSerie()
    except: print('ERROR: Creacion de PuertoSerie')
    try:    puerto.write_ascii(char)
    except: print('ERROR: Funcion write_ascii')
    input('Presione una tecla para continuar...')
    time.sleep(0.2)
    try:    print('Enviado: %s. Recibido %s.' %(char, puerto.read_ascii()))
    except: print('ERROR: Funcion read_ascii')
    puerto.close()

def test_echo_dec(num):
    try:    puerto = puertoSerie.PuertoSerie()
    except: print('ERROR: Creacion de PuertoSerie')
    try:    puerto.write_dec(num)
    except: print('ERROR: Funcion write_dec')
    time.sleep(0.1)
    try:    print('Enviado: %d. Recibido %d.' %(num,puerto.read_dec()))
    except: print('ERROR: Funcion read_dec')
    puerto.close()



def test_read_n():
    n = 512
    char = 'a'
    array = np.zeros(n)
    try:    puerto = puertoSerie.PuertoSerie()
    except: print('ERROR: Creacion de PuertoSerie')
    try:    puerto.write_ascii(char)
    except: print('ERROR: Funcion write_ascii')
    time.sleep(0.1)
    try:    array = puerto.read_n(array)
    except: print('ERROR: Funcion read_n')
    print(array)
    print(np.size(array))



test_echo_ascii('A')
#test_echo_dec()
#test_read_n()
