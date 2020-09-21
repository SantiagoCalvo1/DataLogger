import sqlite3
import numpy as np

class BDatos:
    """ Clase: base de datos. Central en el diseño """
    def __init__(self):
        try:
            self.con = sqlite3.connect('database.db')
            self.cur = self.con.cursor()
        except Exception as e:
            print('ERROR: __init__. ', e)

    def commit(self):
        self.con.commit() #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        return True

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
                "valor" INTEGER NOT NULL,
                "timestamp" INTEGER /*Revisar esto*/,
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
        self.cur.execute('SELECT * FROM DataLogger')
        for fila in self.cur.fetchall():
            print(fila)
        print()
        self.cur.execute('SELECT * FROM Datos')
        for fila in self.cur.fetchall():
            print(fila)

    def add_n_datos(self, array, dataLogger_id):
        # Falta agregar lo del timestamp (esto solo tiene sentido con el RTC)
        try:
            for i in range(np.size(array)):
                self.cur.execute('''
                INSERT INTO Datos (valor, timestamp, dataLogger_id) 
                VALUES (?, ?, ?);
                ''', (array[i], None, dataLogger_id))
            self.commit()
            return True
        except Exception as e:
            print("Excepción: bDatos -> add_n_datos", e, sep=" ")
            return False