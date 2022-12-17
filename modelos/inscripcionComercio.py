import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='muni2'
)

cursor = conn.cursor()

class Comercio():
    def __init__(self) -> None:
        self.nombrecomercio = None
        self.telefonocomercial = None
        self.direccioncomercio = None
        self.pagina = None
        self.categoria = None
    
    def listarComercios(self):
        cursor.execute ('SELECT * FROM inscripciongeneral')
        todasInscrip = cursor.fetchall()
        return todasInscrip
    
    def borrarComercio(self,nombre):
        cursor.execute('DELETE FROM inscripciongeneral WHERE nombrecomercio = %s',(nombre))
        conn.commit()