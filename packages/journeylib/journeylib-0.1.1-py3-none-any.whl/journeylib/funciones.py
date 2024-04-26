#Imports necesarios para las funciones de la libreria
import requests

#Metodo de prueba para el despliege de la libreria
def hola_journey():
    print('Holitaa, esta es una librería diseñada y publicada por JourneyGen.')



#Implementacion de las funciones necesarias para la libreria
url_por_especificar = 'http://servidor:puerto/endpoint'
"""
METODO INSERTAR HISTORICO
Descripcion: Inserta un nuevo par de mensajes a la bd de CASH
"""
def ins_historico(usr, num_chat, lista_msg, url=url_por_especificar):
    
    datos_post = { # Formato con el que se consume la api
        'id_usuario': usr,
        'num_chat': num_chat,
        'msg': lista_msg
    }

    return requests.post(url, json=datos_post)