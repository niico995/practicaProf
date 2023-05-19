import pymysql
conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    db="municipalidad",
)

cursor = conn.cursor()

class Usuario():
    def __init__(self) -> None:
        self.nombre = None
        self.correo = None
        self.contraseña = None
    
#Consulta para listar todos los usuarios creados.
    def listadoUsuarios(self):
        cursor.execute('SELECT* FROM usuarios')
        todosUsuarios = cursor.fetchall()
        
        return todosUsuarios

#Consulta para validar si es un correo existente.
    def obtenerUsuario(self,correo):
        cursor.execute('SELECT correo FROM usuarios WHERE correo = %s', (correo))
        correoValido = cursor.fetchone()
        
        return correoValido

#Consulta para obtener el nombre de usuario, para mensaje de bienvenida.
    def obtenerNombre(self,correo):
        cursor.execute('SELECT nombre FROM usuarios WHERE correo = %s', (correo))
        nombreUsuario = cursor.fetchone()
        
        return nombreUsuario

#Conuslta para validar si la contraseña es correcta.
    def obtenerContraseña(self,correo,contraseña):
        cursor.execute('SELECT contraseña FROM usuarios WHERE correo = %s AND contraseña = %s', (correo,contraseña))
        usuarioValido = cursor.fetchone()
        
        return usuarioValido
    
    def obtenerContraseña2(self,correo):
        cursor.execute('SELECT contraseña FROM usuarios WHERE correo = %s', (correo))
        usuarioValido = cursor.fetchone()
        
        return usuarioValido
    

#Consulta para agregar un usuario.
    def agregarUsuario(self,usuario):
        cursor.execute('INSERT INTO usuarios VALUES (%s,%s,%s)', (usuario.nombre,usuario.correo,usuario.contraseña))
        conn.commit()
        

#Consulta para cambiar la contraseña
    def cambiarContraseña(self,contraseña,correo):
        cursor.execute('UPDATE usuarios SET contraseña = %s WHERE correo = %s',(contraseña,correo))
        conn.commit()
        

    
    
    

    

