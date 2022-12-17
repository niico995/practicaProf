import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='municipalidad'
)

cursor = conn.cursor()

class Artesano():
    def __init__(self) -> None:
        self.dni = None
        self.nombre = None
        self.apellido = None
        self.telefono = None
        self.barrio = None
        self.calle = None
        self.numero = None
        self.pagina = None
        self.rubro = None
    
    def listarArtesano(self):
        cursor.execute ('SELECT * FROM inscripcionartesano')
        todosArtesanos = cursor.fetchall()
        return todosArtesanos
    
    def borrarArtesano(self,dni):
        cursor.execute('DELETE FROM inscripcionartesano WHERE dni = %s',(dni))
        conn.commit()