import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='municipalidad'
)

cursor = conn.cursor()

class Servicios():
    def __init__(self) -> None:
        self.nombre = None
        self.direccion = None
        self.telefono = None
        self.categoria = None
        self.ubicacion = None
    
    def listarServicios(self):
        cursor.execute ('SELECT * FROM servicios')
        todosServicios = cursor.fetchall()
        return todosServicios

    def servicios(self,nombre):
        cursor.execute('SELECT * FROM servicios WHERE nombre = %s', (nombre))
        servicioSeleccionado = cursor.fetchone()
        return servicioSeleccionado
    
    def modificarDatos(self,nuevoNombre,nombre,direccion,telefono,ubicacion):
        cursor.execute('UPDATE servicios SET nombre =%s,direccion = %s, telefono = %s, ubicacion = %s WHERE nombre = %s', (nuevoNombre,direccion,telefono,ubicacion,nombre)) 
        conn.commit()

    
    def modificarCategoria(self,nombre,categoria):
        cursor.execute('UPDATE servicios SET categoria = %s WHERE nombre = %s', (categoria,nombre))
        conn.commit()

    def agregarServicio(self,servicio):
        cursor.execute('INSERT INTO servicios VALUES (%s,%s,%s,%s,%s)', (servicio.nombre, servicio.direccion, servicio.telefono,servicio.categoria, servicio.ubicacion))
        conn.commit()
    
    def borrarServicio(self,nombre):
        cursor.execute('DELETE FROM servicios WHERE nombre = %s',(nombre))
        conn.commit()