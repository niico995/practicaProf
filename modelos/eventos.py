import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    db='municipalidad'
)

cursor = conn.cursor()

class Eventos():
    def __init__(self) -> None:
        self.nombreEvento = None
        self.fechaEvento = None
        self.descripcionEvento = None
       
    
    def listarEventos(self):
        cursor.execute ('SELECT * FROM eventos')
        todosEventos = cursor.fetchall()
        return todosEventos

    def eventos(self,nombre):
        cursor.execute('SELECT * FROM eventos WHERE nombreEvento = %s', (nombre))
        eventosSeleccionado = cursor.fetchone()
        return eventosSeleccionado
    
    def modificarDatos(self,nuevoNombre,nombre,fecha,descripcion):
        cursor.execute('UPDATE eventos SET nombreEvento = %s, fechaEvento = %s, descripcionEvento = %s WHERE nombreEvento = %s', (nuevoNombre,fecha,descripcion,nombre)) 
        conn.commit()

    def agregarEvento(self,evento):
        cursor.execute('INSERT INTO eventos VALUES (%s,%s,%s)',(evento.nombreEvento,evento.fechaEvento,evento.descripcionEvento))
        conn.commit()
        
    def borrarEvento(self,nombre):
        cursor.execute('DELETE FROM eventos WHERE nombreEvento = %s',(nombre))
        conn.commit()
