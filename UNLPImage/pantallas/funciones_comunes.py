import io
import PIL
from PIL import Image,ImageDraw
import base64
import numpy as np
import os
import csv
import datetime
import PySimpleGUI as sg

'''
Funciones utilizadas en varias pantallas
'''

def imagen_redonda(image_path):
    '''
    Convierte una la imagen que se pasa como ruta en una imagen redonda
    '''
    # Abrimos la imagen y la convertimos a formato RGB
    img = PIL.Image.open(image_path).convert("RGB")
    # Convertimos la imagen a un arreglo numpy
    arrImg = np.array(img)
    # Creamos una nueva imagen con canal alpha
    alph = PIL.Image.new('L', img.size, 0)
    # Creamos un objeto para dibujar en la nueva imagen
    draw = PIL.ImageDraw.Draw(alph)
    # Creamos un círculo
    draw.pieslice([0, 0, img.size[0], img.size[1]], 0, 360, fill = 255)
    # Convertimos la imagen con alpha a un arreglo numpy
    arAlpha = np.array(alph)
    # Agregamos el canal alpha a la imagen
    arrImg = np.dstack((arrImg, arAlpha))
    # Creamos una nueva imagen a partir del arreglo numpy, en modo RGBA
    return PIL.Image.fromarray(arrImg, mode='RGBA')


def imagen_boton(image_path, resize=None, round=False):
    '''
    Convierte la imagen que se pasa como ruta o en base64 a un formato aceptado
    por los botones de pysimplegui (base64). Ademas acepta parametros para indicar
    si se le hace un resize o si se convierte en una imagen redonda
    '''
    # Se fija si se pasa un path
    if isinstance(image_path, str):
        if round == True:
            img = imagen_redonda(image_path)
        else:
            img = PIL.Image.open(image_path)
    else:
        # Si la imagen es un base64, la decodificamos y la abrimos
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(image_path)))
        except Exception as e:
            # Si no podemos decodificarla, la abrimos con io.BytesIO()
            data_bytes_io = io.BytesIO(image_path)
            img = PIL.Image.open(data_bytes_io)
    
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        # En caso de querer manterer el aspect ratio de la imagen, descomentar las siguiente lineas:
            # scale = min(new_height/cur_height, new_width/cur_width)
            # img = img.resize((int(cur_width*scale), int(cur_height*scale))), PIL.Image.ANTIALIAS)
        img = img.resize((new_width,new_height))
    
    # Convertimos la imagen a un bytes object y lo retornamos
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def normalizar_path(path):
    '''
    Devuelve el path ingresado cambiando las barras dobles por el separador que utiliza el sistema operativo.
    '''
    return path.replace("\\", os.path.sep)


def actualizar_logs(operacion,usuario,valores="",textos=""):
    '''
    Actualiza el csv de logs segun la operación y el usuario que se le pase como parámetro.
    '''
    ruta_archivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos_app", "logs.csv")
    
    nombre = usuario['Nick']
    fechayhora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    nueva_fila = {
        'operacion': operacion,
        'perfil': nombre,
        'fecha actualizacion': fechayhora,
        'valores': valores,
        'textos': textos
    }

    with open(ruta_archivo, mode='a', newline='') as archivo:
        escritor_csv = csv.DictWriter(archivo, fieldnames=nueva_fila.keys())
        escritor_csv.writerow(nueva_fila)


def is_image(file_path):
    '''
    Checkea que la ruta ingresada sea de una imagen.
    '''
    try:
        with Image.open(file_path) as img:
            return True
    except (IOError, SyntaxError) as e:
        return False


def boton_volver(window):
    '''
    Le agrega la imagen al botón de volver.
    '''
    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "back.png")
    image_64 = imagen_boton(image,resize=(40,40))
    window["-VOLVER-"].update(image_data=image_64, button_color=sg.theme_background_color())