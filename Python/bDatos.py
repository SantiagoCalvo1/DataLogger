import sqlite3
import numpy as np

class BDatos:
    """ Clase: base de datos. Central en el diseño """
    def __init__(self):
        try:
            self.con = sqlite3.connect('database.db')
            #self.con = sqlite3.connect('a')
            self.cur = self.con.cursor()
        except Exception as e:
            print('ERROR: __init__. ', e)

    def commit(self):
        self.con.commit() #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        return True

    def sql(self, comando):
        if comando.strip() == '.schema':
            # Ejetuta la función para mostrar el schema de la base de datos
            self.__schema()
        else:
            # Para comandos en SQL:
            try:
                self.cur.execute(comando)
                lista = self.cur.fetchall()
                if len(lista) != 0:
                    # Es decir que fue una operación del tipo SELECT
                    return lista
                else:
                    # Es decir que fue una operación del tipo INSERT:
                    #self.commit()
                    return True
            except Exception as e:
                print('Excepción: bDatos -> sql', e, sep=' ')

    def __schema(self):
        """ Muestra el esquema de la base de datos """
        print('SCHEMA')
        tablas = []
        temp = self.sql('SELECT name FROM sqlite_schema WHERE type="table" ORDER BY name;')
        if self.is_list(temp):
            for i in range(len(temp)):
                if temp[i][0] != 'sqlite_sequence':
                    tablas.append(temp[i][0])
        #print(tablas)
        columnas = []
        for i in range(len(tablas)):
            print('TABLE    ->   %s' %tablas[i])   # Nombre de la tabla
            # PRAGMA table_info:    column_id, name, type, notnull, default_value, pk
            string = 'PRAGMA table_info(%s);' %(tablas[i])
            temp = self.sql(string)
            for j in range(len(temp)):
                numero = temp[j][0]
                nombre = temp[j][1] # Nombre columna
                tipo = temp[j][2]   # Tipo de dato
                if temp[j][3] == 1: # NOT NULL?
                    notnull = 'NOT NULL'
                else:
                    notnull = ''
                if temp[j][5] == 1: # PK?
                    pk = 'PRIMARY KEY'
                else:
                    pk = ''
                print('column %d ->   %s: %s, %s, %s' %(numero, nombre, tipo, notnull, pk))                       
            print()


    def is_bool(self, dato):
        try:
            if type(dato) == bool:
                return True
            else:
                return False
        except Exception as e:
            print('Excepción: bDatos -> is_bool', e, sep=' ')
            return False

    def is_list(self, dato):
        try:
            if type(dato) == list:
                return True
            else:
                return False
        except Exception as e:
            print('Excepción: bDatos -> is_list', e, sep=' ')
            return False


    def reinicializar_db(self):
        self.cur.execute('''DROP TABLE IF EXISTS DataLogger''')
        self.cur.execute('''DROP TABLE IF EXISTS Datos''')
        self.cur.execute('''
            /*  CREAR ESTRUCTURA DE BASE DE DATOS   */
            /* Crear tabla DataLogger */
            CREATE TABLE "DataLogger"(
                "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                "nombre" TEXT NOT NULL UNIQUE,
                "descripcion" TEXT,
                "mail" TEXT
            );
            ''')
        self.cur.execute('''
            /* Crear tabla Datos */
            CREATE TABLE "Datos"(
                "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                "valor" REAL NOT NULL,
                "timestamp" NUMERIC /*Revisar esto*/,
                "dataLogger_id" INTEGER NOT NULL	
            );
            ''')
        self.cur.execute('''
            INSERT INTO DataLogger (nombre, descripcion, mail) 
            VALUES ("dataL_prueba1", "descrpcion1", "prueba1@gmail.com");
            ''')
        self.cur.execute('''
            INSERT INTO DataLogger (nombre, descripcion, mail) 
            VALUES ("dataL_prueba2", "descrpcion2", "prueba2@gmail.com");
            ''')
        self.commit()
        
        rng = np.random.default_rng()
        dL1_size = 100
        dL2_size = 10
        array_dL1 = rng.standard_normal(dL1_size) + 10  # dist normal alrededor de 10
        array_dL2 = rng.standard_normal(dL2_size)       # dist normal alrededor de 0
        array_timestamp_dL1 = []
        array_timestamp_dL2 = []
        for i in range(dL1_size):
            # Array dL1 tomado en el rango '1900-01-01 00:00:0' a '1999-01-01 00:00:00'
            array_timestamp_dL1.append(('%s-%s-%s %s:%s:%s' %(str(1900+i),'01','01','00','00','00'))) 
            #'YYYY-MM-DD HH:MM:SS'
        for i in range(dL2_size):
            # Array dL1 tomado en el rango '2020-09-21 10:15:0' a '2020-09-21 10:15:09'
            array_timestamp_dL2.append(('%s-%s-%s %s:%s:%s' %('2020','09','21','10','15','0'+str(i))))    
            #'YYYY-MM-DD HH:MM:SS'
        self.add_n_datos(array_dL1, array_timestamp_dL1, "dataL_prueba1")
        self.add_n_datos(array_dL2, array_timestamp_dL2, "dataL_prueba2")


    def get_datalogger_id(self, nombre):
        self.cur.execute('SELECT id FROM DataLogger WHERE nombre=?', (nombre,))
        id_dL = self.cur.fetchone()
        if type(id_dL) == tuple:
            return id_dL[0]
        else:
            return False


    def add_n_datos(self, array_datos, array_timestamp, dataLogger_name):
        try:
            dataLogger_id = self.get_datalogger_id(dataLogger_name)
            #dataLogger_id = 'dataL_prueba1'
            if dataLogger_id != False:
                if np.size(array_datos) == len(array_timestamp):
                    for i in range(np.size(array_datos)):
                        self.cur.execute('''
                        INSERT INTO Datos (valor, timestamp, dataLogger_id) 
                        VALUES (?, datetime(?), ?);
                        ''', (array_datos[i], array_timestamp[i], dataLogger_id))
                    self.commit()
                    return True
                else:
                    print('El tamaño del array de datos es diferente al de timestamps. Deben ser iguales.')
                    return False
            else:
                print('No existe un datalogger con ese nombre.')
                return False
        except Exception as e:
            print("Excepción: bDatos -> add_n_datos", e, sep=" ")
            return False

    """
    def get_ultimo_mes(self, dataLogger_id):
        try:
            self.cur.execute('''
                SELECT valor, timestamp FROM Datos
                WHERE dataLogger_id = ? AND
                timestamp BETWEEN datetime('now','start of month')
                AND datetime('now','start of month','+1 month','-1 day', '23 hours', '59 minutes', '59 seconds'); 
                ''', (dataLogger_id,))
            lista = []
            for fila in self.cur.fetchall():
                lista.append(fila)
            return lista
        except Exception as e:
            print("Excepción: bDatos -> get_ultimo_mes", e, sep=" ")
            return False

    def get_ultima_semana(self, dataLogger_id):
        ''' AYUDA PARA GET_ULTIMA SEMANA '''
        try:
            self.cur.execute('''
                SELECT valor, timestamp FROM Datos
                WHERE dataLogger_id = ? AND
                timestamp BETWEEN datetime('now', '-7 day', '00 hours', '00 minutes', '00 seconds')
                AND datetime('now'); 
                ''', (dataLogger_id,))
            lista = []
            for fila in self.cur.fetchall():
                lista.append(fila)
            return lista
        except Exception as e:
            print("Excepción: bDatos -> get_ultimo_mes", e, sep=" ")
            return False

    def get_dia_actual(self, dataLogger_id):
        try:
            self.cur.execute('''
                SELECT valor, timestamp FROM Datos
                WHERE dataLogger_id = ? AND
                timestamp BETWEEN datetime('now', 'start of day', '00 hours', '00 minutes', '00 seconds')
                AND datetime('now', 'start of day', '23 hours', '59 minutes', '59 seconds'); 
                ''', (dataLogger_id,))
            lista = []
            for fila in self.cur.fetchall():
                lista.append(fila)
            return lista
        except Exception as e:
            print("Excepción: bDatos -> get_dia_actual", e, sep=" ")
            return False
    """