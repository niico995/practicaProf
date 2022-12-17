import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='municipalidad'
)

cursor = conn.cursor()

class Gastronomia():
    def __init__(self) -> None:
        self.nombre = None
        self.direccion = None
        self.telefono = None
        self.pagina = None
        self.categoria = None
        self.ubicacion = None
    
    def listarGastronomicos(self):
        cursor.execute ('SELECT * FROM gastronomia')
        todosGastronomicos = cursor.fetchall()
        return todosGastronomicos

    def gastronomia(self,nombre):
        cursor.execute('SELECT * FROM gastronomia WHERE nombre = %s', (nombre))
        gastronomicoSeleccionado = cursor.fetchone()
        return gastronomicoSeleccionado
    
    def modificarDatos(self,nuevoNombre,nombre,direccion,telefono,pagina,ubicacion):
        cursor.execute('UPDATE gastronomia SET nombre = %s, direccion = %s, telefono = %s, pagina = %s, ubicacion = %s WHERE nombre = %s', (nuevoNombre,direccion,telefono,pagina,ubicacion,nombre)) 
        conn.commit()

    
    def modificarCategoria(self,nombre,categoria):
        cursor.execute('UPDATE gastronomia SET categoria = %s WHERE nombre = %s', (categoria,nombre))
        conn.commit()

    def agregarGastronomico(self,gastronomico):
        cursor.execute('INSERT INTO gastronomia VALUES (%s,%s,%s,%s,%s,%s)', (gastronomico.nombre, gastronomico.direccion, gastronomico.telefono, gastronomico.pagina, gastronomico.categoria, gastronomico.ubicacion))
        conn.commit()
    
    def borrarGastronomico(self,nombre):
        cursor.execute('DELETE FROM gastronomia WHERE nombre = %s',(nombre))
        conn.commit()
