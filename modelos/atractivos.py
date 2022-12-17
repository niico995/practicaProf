import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='municipalidad'
)

cursor = conn.cursor()

class Atractivos():
    def __init__(self) -> None:
        self.nombre = None
        self.direccion = None
        self.telefono = None
        self.pagina = None
        self.categoria = None
        self.ubicacion = None
    
    def listarAtractivos(self):
        cursor.execute ('SELECT * FROM atractivos')
        todosAtractivos = cursor.fetchall()
        return todosAtractivos

    def atractivos(self,nombre):
        cursor.execute('SELECT * FROM atractivos WHERE nombre = %s', (nombre))
        atractivoSeleccionado = cursor.fetchone()
        return atractivoSeleccionado
    
    def modificarDatos(self,nuevoNombre,nombre,direccion,telefono,pagina,ubicacion):
        cursor.execute('UPDATE atractivos SET nombre = %s, direccion = %s, telefono = %s, pagina = %s, ubicacion = %s WHERE nombre = %s', (nuevoNombre,direccion,telefono,pagina,ubicacion,nombre)) 
        conn.commit()

    
    def modificarCategoria(self,nombre,categoria):
        cursor.execute('UPDATE atractivos SET categoria = %s WHERE nombre = %s', (categoria,nombre))
        conn.commit()

    def agregarAtractivo(self,atractivo):
        cursor.execute('INSERT INTO atractivos VALUES (%s,%s,%s,%s,%s,%s)',(atractivo.nombre,atractivo.direccion,atractivo.telefono,atractivo.pagina,atractivo.categoria, atractivo.ubicacion))
        conn.commit()
        
    def borrarAtractivo(self,nombre):
        cursor.execute('DELETE FROM atractivos WHERE nombre = %s',(nombre))
        conn.commit()
