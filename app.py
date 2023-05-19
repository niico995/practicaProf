from flask import Flask, render_template, request, redirect, url_for, flash, session
from modelos.usuarios import Usuario
from modelos.alojamientos import Alojamiento
from modelos.gastronomia import Gastronomia
from modelos.atractivos import Atractivos
from modelos.servicios import Servicios
from modelos.eventos import Eventos
from modelos.inscripArtesano import Artesano
from modelos.inscripcionComercio import Comercio
from flask_session import Session
from flask_socketio import SocketIO
from funciones.cambio import enviarMail,encriptar,comprobar,contraseñaRandom,rutaMaps
from werkzeug.utils import secure_filename
import os
import shutil
 


usuario = Usuario()
alojamiento = Alojamiento()
gastronomico = Gastronomia()
atractivo = Atractivos()
servicio = Servicios()
evento = Eventos()
artesano = Artesano()
comercio = Comercio()


app = Flask(__name__)
app.secret_key = 'we love wawas'
app.config['SESSION_PERMANENT']= False
app.config['SESSION_TYPE']='filesystem'
Session(app)
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = 'C:/Users/NicoJuarez/Documents/vistaUsuario/static/banners'



#----------------------Inicio ruta de incio de session
@app.route('/')
def login():
    return render_template('login.html')


#--------------------Comprobación de datos
@app.route('/datosUsuario',methods=['GET','POST'])
def validarUsuario():
    if request.method == 'POST':
        correo = request.form['correo']
        if usuario.obtenerUsuario(correo) != None:
            contraseña = request.form['contraseña']
            contraBd = usuario.obtenerContraseña2(correo)
            contraBd = contraBd[0]
            if (comprobar(contraseña,contraBd)):
                session['user'] = usuario.obtenerNombre(correo)
                session['loggedin'] = True
                session['username'] = correo
                return redirect(url_for('menu'))

            else:
                flash('Contraseña incorrecta')
                return redirect(url_for('login'))
        else:
            flash('Usuario incorrecto')
            return redirect(url_for('login'))  



#---------------------Ir al panel
@app.route('/home')
def menu():
    if 'user' in session:
        saludo = session['user']
        saludo = saludo[0]
        return render_template('index.html',saludo=saludo)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))
  

@app.route('/index.html')
def irMenu():
    return redirect(url_for('menu'))  



#------------Alojamientos
#-------------Inicio alojamientos----------------
@app.route('/alojamiento')
def alojamientos():
    if 'user' in session:
        listadoAlojamientos = alojamiento.listarAlojamientos()
        return render_template('alojamiento.html', listados=listadoAlojamientos)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))

@app.route('/alojamiento.html')
def irAlojamiento():
    return redirect(url_for('alojamientos'))

#------------Editar Alojamientos----------------
@app.route('/editar/<string:nombre>')
def alojamientoEditar(nombre):
    alojamientoEditar = alojamiento.alojamiento(nombre)
    return render_template('alojamientoEditar.html', alojamiento=alojamientoEditar)


@app.route('/alojamientoLista', methods=['POST'])
def volverListaAloj():
    if request.method == 'POST':
        return redirect(url_for('alojamientos'))


@app.route('/cambiarDatos/<string:nombre>', methods=['POST'])
def cambiarDatos(nombre):
    if request.method == 'POST':
        nombre = nombre
        nombreAloj = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        pagina = request.form['pagina']
        categoria = request.form['categoria']
        ubicacion = request.form['ubicacion']
        try:
            ubicacion = rutaMaps(ubicacion)
            alojamiento.modificarCategoria(nombreAloj,categoria)
            alojamiento.modificarDatos(nombreAloj,nombre,direccion,telefono,pagina,ubicacion)
        except:
            alojamiento.modificarCategoria(nombreAloj,categoria)
            alojamiento.modificarDatos(nombreAloj,nombre,direccion,telefono,pagina,ubicacion)
        return redirect(url_for('alojamientos'))


#----------Agregar Alojamiento----------------
@app.route('/agregarAlojamiento')
def irAgregar():
    if 'user' in session:
        return render_template('alojamientoAgregar.html')
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))

@app.route('/agregarAlojamiento', methods=['POST'])
def agregarAlojamiento():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if alojamiento.alojamiento(nombre):
            flash('Este alojamiento ya fue registrado')
            return redirect(url_for('irAgregar'))
        else:
            nuevoAlojamiento = Alojamiento()
            nuevoAlojamiento.nombre = request.form['nombre']
            nuevoAlojamiento.direccion = request.form['direccion']
            nuevoAlojamiento.telefono = request.form['telefono']
            nuevoAlojamiento.pagina = request.form['pagina']
            nuevoAlojamiento.categoria = request.form['categoria']
            ubicacion = request.form['ubicacion']
            ubicacion = rutaMaps(ubicacion)
            nuevoAlojamiento.ubicacion = ubicacion
            alojamiento.agregarAlojamiento(nuevoAlojamiento)
            return redirect(url_for('alojamientos'))

#---------Borrar Alojamiento----------------
@app.route('/borrar/<string:nombre>')
def borrarAlojamiento(nombre):
    alojamiento.borrarAlojamiento(nombre)
    return redirect(url_for('alojamientos'))



#----------------Gastronomia
#----------------Inicio Gastronomia----------------
@app.route('/gastronomia')
def gastronomia():
    if 'user' in session:
        listadoGastronomia = gastronomico.listarGastronomicos()
        return render_template('gastronomia.html', listados=listadoGastronomia)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/gastronomia.html')
def irGastronomia():
    return redirect(url_for('gastronomia'))


#--------------------Agregar gastronomico----------------
@app.route('/agregarGastronomico')
def irAgregarG():
    if 'user' in session:
        return render_template('gastronomiaAgregar.html')
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/agregarGastronomicco', methods=['POST'])
def agregarGastronomico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if gastronomico.gastronomia(nombre):
            flash('Este local ya fue registrado')
            return redirect(url_for('irAgregarG'))
        else:
            nuevoGastronomico = Gastronomia()
            nuevoGastronomico.nombre = request.form['nombre']
            nuevoGastronomico.direccion = request.form['direccion']
            nuevoGastronomico.telefono = request.form['telefono']
            nuevoGastronomico.pagina = request.form['pagina']
            nuevoGastronomico.categoria = request.form['categoria']
            ubicacion = request.form['ubicacion']
            ubicacion = rutaMaps(ubicacion)
            nuevoGastronomico.ubicacion = ubicacion
            gastronomico.agregarGastronomico(nuevoGastronomico)
            return redirect(url_for('gastronomia'))


#-----------------------Borrar Gastronomico----------------
@app.route('/borrarG/<string:nombre>')
def borrarGastronomico(nombre):
    gastronomico.borrarGastronomico(nombre)
    return redirect(url_for('gastronomia'))


#-----------------------Editar Gastronomico----------------
@app.route('/editarG/<string:nombre>')
def gastronomicoEditar(nombre):
    gastronomiaEditar = gastronomico.gastronomia(nombre)
    return render_template('gastronomiaEditar.html', gastronomia=gastronomiaEditar)
@app.route('/gastronomiaLista', methods=['POST'])
def volverListaG():
    if request.method == 'POST':
        return redirect(url_for('gastronomia'))
@app.route('/cambiarDatosG/<string:nombre>', methods=['POST'])
def cambiarDatosG(nombre):
    if request.method == 'POST':
        nombreGast = nombre
        nuevoNombreG = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        pagina = request.form['pagina']
        categoria = request.form['categoria']
        ubicacion = request.form['ubicacion']
        try:
            ubicacion = rutaMaps(ubicacion)
            gastronomico.modificarCategoria(nombreGast,categoria)
            gastronomico.modificarDatos(nuevoNombreG,nombreGast,direccion,telefono,pagina,ubicacion)
        except:
            gastronomico.modificarCategoria(nombreGast,categoria)
            gastronomico.modificarDatos(nuevoNombreG,nombreGast,direccion,telefono,pagina,ubicacion) 
        
        return redirect(url_for('gastronomia'))



#------------------------------Atractivos
#-----------------------------Inicio Atractivos------------
@app.route('/atractivo')
def atractivos():
    if 'user' in session:
        listadoAtractivos = atractivo.listarAtractivos()
        return render_template('atractivos.html', listados=listadoAtractivos)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/atractivos.html')
def irAtractivos():
    return redirect(url_for('atractivos'))


#----------------------------Editar Atractivos--------------
@app.route('/editarAtract/<string:nombre>')
def atractivoEditar(nombre):
    atractivoEditar = atractivo.atractivos(nombre)
    return render_template('atractivosEditar.html', atractivo=atractivoEditar)


@app.route('/atractivosLista', methods=['POST'])
def volverListaAtrac():
    if request.method == 'POST':
        return redirect(url_for('atractivos'))


@app.route('/cambiarDatosAtrac/<string:nombre>', methods=['POST'])
def cambiarDatosAtract(nombre):
    if request.method == 'POST':
        nombreAtrac = nombre
        nuevoNomAtrac = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        pagina = request.form['pagina']
        categoria = request.form['categoria']
        ubicacion = request.form['ubicacion']
        try:
            ubicacion = rutaMaps(ubicacion)
            atractivo.modificarCategoria(nombreAtrac,categoria)
            atractivo.modificarDatos(nuevoNomAtrac,nombreAtrac,direccion,telefono,pagina,ubicacion)
        except:
            atractivo.modificarCategoria(nombreAtrac,categoria)
            atractivo.modificarDatos(nuevoNomAtrac,nombreAtrac,direccion,telefono,pagina,ubicacion)
        
        return redirect(url_for('atractivos'))


#---------------------------Borrar Atractivo----------------
@app.route('/borrarAtract/<string:nombre>')
def borrarAtractivo(nombre):
    atractivo.borrarAtractivo(nombre)
    return redirect(url_for('atractivos'))


#--------------------Agregar Atractivos----------------
@app.route('/agregarAtractivo')
def irAgregarAtractivos():
    if 'user' in session:
        return render_template('atractivosAgregar.html')
    

@app.route('/agregarAtractivo', methods=['POST'])
def agregarAtractivo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if atractivo.atractivos(nombre):
            flash('Este lugar ya fue registrado')
            return redirect(url_for('irAgregarAtractivo'))
        else:
            nuevoAtractivo = Atractivos()
            nuevoAtractivo.nombre = request.form['nombre']
            nuevoAtractivo.direccion = request.form['direccion']
            nuevoAtractivo.telefono = request.form['telefono']
            nuevoAtractivo.pagina = request.form['pagina']
            nuevoAtractivo.categoria = request.form['categoria']
            ubicacion = request.form['ubicacion']
            ubicacion = rutaMaps(ubicacion)
            nuevoAtractivo.ubicacion = ubicacion
            atractivo.agregarAtractivo(nuevoAtractivo)
            return redirect(url_for('atractivos'))



#-----------------------------Servicios
#-----------------------------Inicio Servicios----------------
@app.route('/servicios')
def servicios():
    if 'user' in session:
        listadoServicios = servicio.listarServicios()
        return render_template('servicios.html', listados=listadoServicios)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/servicios.html')
def irServicios():
    return redirect(url_for('servicios'))


#--------------------Agregar Servicios----------------
@app.route('/agregarServicios')
def irAgregarServ():
    if 'user' in session:
        return render_template('serviciosAgregar.html')
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/agregarServicio', methods=['POST'])
def agregarServicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if servicio.servicios(nombre):
            flash('Este servicio ya fue registrado')
            return redirect(url_for('irAgregarServ'))
        else:
            nuevoServicio = Servicios()
            nuevoServicio.nombre = request.form['nombre']
            nuevoServicio.direccion = request.form['direccion']
            nuevoServicio.telefono = request.form['telefono']
            nuevoServicio.categoria = request.form['categoria']
            ubicacion = request.form['ubicacion']
            ubicacion = rutaMaps(ubicacion)
            nuevoServicio.ubicacion = ubicacion
            servicio.agregarServicio(nuevoServicio)
            return redirect(url_for('servicios'))


#----------------------------Editar Servicios----------------
@app.route('/editarServ/<string:nombre>')
def servicioEditar(nombre):
    servicioEditar = servicio.servicios(nombre)
    return render_template('serviciosEditar.html', servicios=servicioEditar)


@app.route('/serviciosLista', methods=['POST'])
def volverListaServ():
    if request.method == 'POST':
        return redirect(url_for('servicios'))


@app.route('/cambiarDatosServ/<string:nombre>', methods=['POST'])
def cambiarDatosServ(nombre):
    if request.method == 'POST':
        nombreServ = nombre
        nuevoNombreServ = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        categoria = request.form['categoria']
        ubicacion = request.form['ubicacion']
        try:
            ubicacion = rutaMaps(ubicacion)
            servicio.modificarCategoria(nombreServ,categoria)
            servicio.modificarDatos(nuevoNombreServ,nombreServ,direccion,telefono,ubicacion)
        except:
            servicio.modificarCategoria(nombreServ,categoria)
            servicio.modificarDatos(nuevoNombreServ,nombreServ,direccion,telefono,ubicacion)
        
        return redirect(url_for('servicios'))


#---------------------------Borrar Servicios----------------
@app.route('/borrarServ/<string:nombre>')
def borrarServicio(nombre):
    servicio.borrarServicio(nombre)
    return redirect(url_for('servicios'))



#---------------------------Eventos
#-----------------------------Inicio Eventos----------------
@app.route('/eventos')
def eventos():
    if 'user' in session:
        listadoEventos = evento.listarEventos()
        return render_template('eventos.html', listados=listadoEventos)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/eventos.html')
def irEventos():
    return redirect(url_for('eventos'))


#--------------------Agregar Eventos------------------------
@app.route('/agregarEvento')
def irAgregarEventos():
    return render_template('eventosAgregar.html')


@app.route('/agregarEventos', methods=['POST'])
def agregarEventos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if evento.eventos(nombre):
            flash('Este evento ya fue registrado')
            return redirect(url_for('irAgregarEventos'))
        else:
            nuevoEvento = Eventos()
            nuevoEvento.nombreEvento = request.form['nombre']
            nuevoEvento.fechaEvento = request.form['fecha']
            nuevoEvento.descripcionEvento = request.form['descripcion']
            evento.agregarEvento(nuevoEvento)

            file = request.files['banner']
            filename = secure_filename(file.filename)
            extencion = os.path.splitext(filename)[1]
            nuevoNombre = nombre + extencion
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],nuevoNombre))
            return redirect(url_for('eventos'))


#-----------------Editar Eventos-----------------------
@app.route('/editarEventos/<string:nombre>')
def eventosEditar(nombre):
    eventoEditar = evento.eventos(nombre)
    return render_template('eventosEditar.html', eventos=eventoEditar)


@app.route('/eventosLista', methods=['POST'])
def volverListaEventos():
    if request.method == 'POST':
        return redirect(url_for('eventos'))


@app.route('/editarEventos/<string:nombre>', methods=['POST'])
def cambiarDatosEventos(nombre):
    if request.method == 'POST':
        nombreEventos = nombre
        nuevoNombreEvento = request.form['nombre']
        fechaEvento = request.form['fecha']
        descripcionEvento = request.form['descripcion']
        
        # ----Cambiar el banner-------------
        nombreBanner = request.form['nombre']
        file = request.files['banner']
        filename = secure_filename(file.filename)
        extencion = os.path.splitext(filename)[1]
        nuevoNombre = nombreBanner + extencion
        aBorrar = nombreBanner +'.jpg'
        ruta = app.config['UPLOAD_FOLDER']
        os.remove(ruta+'/'+aBorrar)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],nuevoNombre))
        #-----------------------------------
        
        evento.modificarDatos(nuevoNombreEvento,nombreEventos,fechaEvento,descripcionEvento)
        return redirect(url_for('eventos'))


#---------------------Borrar Evento------------------------
@app.route('/borrarEventos/<string:nombre>')
def borrarEvento(nombre):
    
    # ----- Borrar Banner del evento ----
    nombreBanner = nombre
    aBorrar = nombreBanner + '.jpg'
    os.remove(app.config['UPLOAD_FOLDER']+'/'+aBorrar)
    # ----------------------------------
    
    evento.borrarEvento(nombre)
    return redirect(url_for('eventos'))



#----------------------------Usuarios
#---------------------------Inicio Usuarios----------------
@app.route('/usuarios')
def usuarios():
    if 'user' in session:
        listaUsuario = usuario.listadoUsuarios()
        return render_template('usuarios.html', listados=listaUsuario)
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/usuarios.html')
def irUsuarios():
    return redirect(url_for('usuarios'))


#--------------------------Agregar usuarios----------------
@app.route('/agregarUsuario')
def irAgregarUsuario():
    if 'user' in session:
        return render_template('usuarioAgregar.html')
    else:
        flash('Debes estar logueado')
        return redirect(url_for('login'))


@app.route('/agregarUsuario', methods=['POST'])
def agregarUsuario():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        contraConfir = request.form['contraseñaConfir']
        cantidadUsuarios = usuario.listadoUsuarios()
        if len(cantidadUsuarios)>4:
            flash('Se alcanzó el limite de usuarios permitidos')
            return redirect(url_for('irAgregarUsuario'))
        else:
            if usuario.obtenerUsuario(correo):
                flash('Este usuario ya fue registrado')
                return redirect(url_for('irAgregarUsuario'))
            elif contraseña == contraConfir:
                nuevoUsuario = Usuario()
                nuevoUsuario.nombre = request.form['nombre']
                nuevoUsuario.correo = request.form['correo']
                contraseñaH = encriptar(contraseña)
                nuevoUsuario.contraseña = contraseñaH
                usuario.agregarUsuario(nuevoUsuario)
                return redirect(url_for('usuarios'))
            else:
                flash('Las contraseñas ingresadas no coinciden')
                return redirect(url_for('irAgregarUsuario'))


@app.route('/usuariosLista', methods=['POST'])
def volverUsuarios():
    if request.method == 'POST':
        return redirect(url_for('usuarios'))

#---------------------------------Artesanos
@app.route('/inscripcionArtesano')
def inscripcionArtesano():
    artesanos = artesano.listarArtesano()
    return render_template('inscripcionArtesano.html',artesanos=artesanos)


@app.route('/inscripcionArtesano.html')
def irIncripcionArtesano():
    return redirect(url_for('inscripcionArtesano'))

@app.route('/borrarAr/<int:dni>')
def borrarInscripcion(dni):
    artesano.borrarArtesano(dni)
    return redirect(url_for('inscripcionArtesano'))


#---------------------------Comercios
@app.route('/inscripcionComercio')
def inscripcionComercio():
    comercios = comercio.listarComercios()
    return render_template('inscripcionComercio.html', comercios = comercios)


@app.route('/inscripcionComercio.html')
def irIncripcionComercio():
    return redirect(url_for('inscripcionComercio'))

@app.route('/borrarComercio/<string:nombrecomercio>')
def borrarInscripcionC(nombrecomercio):
    comercio.borrarComercio(nombrecomercio)
    return redirect(url_for('inscripcionComercio'))




#----------------Cierre de sesión para navegador 
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@socketio.on('disconnect')
def disconnect_user():
    session.pop('user',None)

#-------------Botón cierre de sesión
@app.route('/cerrarSesion',methods=['POST'])
def cerrarSesion():
    if request.method == 'POST':
        return redirect(url_for('logout'))


#-------------Inicio recuperar contraseña---Ir menú
@app.route('/recuperar')
def recuperar():
    return render_template('recupContraseña.html')

@app.route('/recupContraseña.html')
def irRecuperar():
    return redirect(url_for('recuperar'))


#--------Enviar correo con contraseña aleatoria
@app.route('/datosRecuperar', methods=['POST'])
def enviarCorreo():
    if request.method == 'POST':
        correo = request.form['correo']
        if usuario.obtenerUsuario(correo):
            contraseñaR = contraseñaRandom()
            enviarMail(contraseñaR,correo)
            session['user'] = correo
            
#-------Encriptar contraseña------------------------------------
            contraseñaR = encriptar(contraseñaR)
            usuario.cambiarContraseña(contraseñaR,correo)
            return redirect(url_for('contraseñaRecibida'))
        
        else:
            flash('Correo no encontrado')
            return redirect(url_for('recuperar'))


#------Recibe y comprueba la contraseña nueva
@app.route('/contraseñaNueva',methods=['POST'])
def cambiarContraseña():
    if request.method == 'POST':
        contraseña1 = request.form['contraseñaCambiar']
        contraseña2 = request.form['contraseñaConfirmar']

#-------Encriptamos la contraseña nueva       
        if contraseña1 == contraseña2:
            correo = session['user']
            contraseña1 = encriptar(contraseña1)
            usuario.cambiarContraseña(contraseña1,correo)
            flash('Ingrese con su nueva contraseña')
            return redirect(url_for('login'))
        
        else:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('nuevaContraseña'))

#------Ir confirmar contraseña-----------------------
@app.route('/nuevaContraseña')
def nuevaContraseña():
    return render_template('confirmarContraseña.html')

#-----Comprobar contraseña recibida
@app.route('/contraseñaRecibida')
def contraseñaRecibida():
    return render_template('confirmarContraRandom.html')


#-----Comprobar contraseña recibida con la contraseña encriptada
@app.route('/contraseñaTemporal',methods=['POST'])
def validarContraseña():
    if request.method == 'POST':
        contraseñaTempo = request.form['contraseñaCambiar']
        correo = session['user']
        contraseñaTempoGuardada = usuario.obtenerContraseña2(correo)
        contraseñaTempoGuardada = contraseñaTempoGuardada[0]
        if (comprobar(contraseñaTempo,contraseñaTempoGuardada)):
            return redirect(url_for('nuevaContraseña'))
        
        else:
            flash('La contraseña es incorrecta')
            return redirect(url_for('contraseñaRecibida'))















#-----Inicio de la aplicación
if __name__ == '__main__':
    app.run(port=5400,debug=True)
    
