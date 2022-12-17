import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='municipalidad'
)

cursor = conn.cursor()

class Alojamiento():
    def __init__(self) -> None:
        self.nombre = None
        self.direccion = None
        self.telefono = None
        self.pagina = None
        self.categoria = None
        self.ubicacion = None
    
    def listarAlojamientos(self):
        cursor.execute ('SELECT * FROM alojamiento')
        todosAlojamientos = cursor.fetchall()
        return todosAlojamientos

    def alojamiento(self,nombre):
        cursor.execute('SELECT * FROM alojamiento WHERE nombre = %s', (nombre))
        alojamientoSeleccionado = cursor.fetchone()
        return alojamientoSeleccionado
    
    def modificarDatos(self,nombre,nombrealoj,direccion,telefono,pagina,ubicacion):
        cursor.execute('UPDATE alojamiento SET nombre = %s, direccion = %s, telefono = %s, pagina = %s, ubicacion = %s WHERE nombre = %s', (nombre,direccion,telefono,pagina,ubicacion,nombrealoj)) 
        conn.commit()

    
    def modificarCategoria(self,nombre,categoria):
        cursor.execute('UPDATE alojamiento SET categoria = %s WHERE nombre = %s', (categoria,nombre))
        conn.commit()

    def agregarAlojamiento(self,alojamiento):
        cursor.execute('INSERT INTO alojamiento VALUES (%s,%s,%s,%s,%s,%s)', (alojamiento.nombre, alojamiento.direccion, alojamiento.telefono, alojamiento.pagina, alojamiento.categoria, alojamiento.ubicacion))
        conn.commit()
    
    def borrarAlojamiento(self,nombre):
        cursor.execute('DELETE FROM alojamiento WHERE nombre = %s',(nombre))
        conn.commit()


