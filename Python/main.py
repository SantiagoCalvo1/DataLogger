import os
import bDatos
import pSerie
import matplotlib.pyplot as plt

print('''
#####
Bienvenido al shell para el uso del Data Logger!
Este se comporta como el shell de Python3.
Los objetos para trabajar son:
    db  ->  Objeto base de datos.
    com ->  Objeto comunicación serie.
    plt ->  Objeto matplotlib.pyplot para gráficas.
#####
''')
# Inicializar base de datos
db = bDatos.BDatos()

# Inicializar analisis de datos (import matplotlib.pyplot as plt)

#Inicializar Puerto Serie
try:
    if os.name == 'nt': # Windows
        com = pSerie.PSerie(port='COM4')
    else:               # Linux (os.name = 'posix')
        com = pSerie.PSerie(port='/dev/ttyACM0')
except Exception as e:
    print('''ERROR: No se tiene acceso al Puerto Serie.
Verifique que esté bien conectado y/o que no haya otro programa utilizandolo.\n''',
'Exception: ', e, sep='')
    try:
        com = pSerie.PSerie(port=input('Introduzca el nombre del puerto serie: ').strip().upper())
        print('Se ha conectado con éxito!')
    except Exception as e:
        print('Se desactivan las funciones de comunicación. Para volver a intentar reinicie el programa.\n',
        'Exception: ', e, sep='')

# linea para ejecutar código directamente en el shell de python, sin import
# esto no sirve de nada ahora pero podria ser útil (22/09)
#exec(open("D:\\workspaces\PROYECTOS\DataLogger\Python\main.py").read()) 

#### FUNCIONES VARIAS ####
def clear():
    ''' Función equivalente a CLS en Windows y clear en UNIX '''
    if os.name == 'nt': # Windows
        _ = os.system('cls')
    else:               # Linux (os.name = 'posix')
        _ = os.system('clear')


