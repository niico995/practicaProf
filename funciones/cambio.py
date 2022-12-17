from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Flask,current_app
import random
import string


correos = Flask(__name__)

correos.config['MAIL_SERVER']='smtp.gmail.com'
correos.config['MAIL_PORT']=465
correos.config['MAIL_USERNAME']='proyectofinalitse@gmail.com'
correos.config['MAIL_PASSWORD']='rtdlmmuykpntztfz'
correos.config['MAIL_USE_TLS']=False
correos.config['MAIL_USE_SSL']=True
mail = Mail(correos)


#Función para encriptar la contraseña
def encriptar(contraseña):
    contraseñaEncrip = generate_password_hash(contraseña,'sha256',15)
    return contraseñaEncrip

#Función para comprobar si la contraseña ingresada es igual a la de la BD
def comprobar(contraseña,encriptado):
    if (check_password_hash(encriptado,contraseña)):
        return True
    else:
        return False
    #return check_password_hash(encriptado,contraseña)

#Función para enviar el correo con la contraseña temporal
def enviarMail(mensaje,correo):
    msg = Message(
    subject = ('Recuperación de contraseña'),
    sender = 'proyectofinalitse@gmail.com',
    recipients = [correo],
    body = f'Su clave temporal es {mensaje}')
    mail.send(msg)
    return print('Enviado')

def contraseñaRandom():
    contraRandom = ''.join(random.sample(string.ascii_letters,8))
    return contraRandom



#Recortar la ruta del maps

def rutaMaps(link):
    aRecortar = link.split(' ')
    recortado = aRecortar[1]
    recortado = recortado.split('"')
    recortado = recortado[1]
    return recortado