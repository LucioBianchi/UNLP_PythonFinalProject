import PySimpleGUI as sg
from pantallas import etiquetar_imagenes, seleccionador_collage, seleccionador_memes, editar_perfil, configuracion, inicio
from pantallas import constantes as const
from . funciones_comunes import imagen_boton
import json
import os


def mostrar_imagenes_botones(window,usuario):
    '''
    Actualiza las imagenes de varios botones
    '''
    image = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), usuario["Avatar"])
    image_64 = imagen_boton(image,resize=const.TAM_PERFILES,round=True)
    window["-EDITAR PERFIL-"].update(image_data=image_64, button_color=sg.theme_background_color())

    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "config.png")
    image_64 = imagen_boton(image,resize=const.TAM_PERFILES)
    window["-CONFIGURACION-"].update(image_data=image_64, button_color=sg.theme_background_color())

    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "help.png")
    image_64 = imagen_boton(image,resize=const.TAM_PERFILES)
    window["-AYUDA-"].update(image_data=image_64, button_color=sg.theme_background_color())


def abrir_dirs():
    '''
    Devuelve los valores de los directorios de imagenes, collage y memes
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","dirs.json"), "r") as dirs:
        data = json.load(dirs)
        return data["Dir Imagenes"], data["Dir Collage"], data["Dir Memes"]


def mostrar_mensaje_ayuda():
    '''
    Hace un Popup con un mensaje que explica como se utiliza la aplicación
    '''
    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "help.png")
    image = imagen_boton(image,resize=(10,10))

    # Esta línea no respeta la guía de estilos, pero porque sino PySimpleGui no justifica el texto
    sg.Popup("¡Bienvenido/a a UNLPImage! Esta aplicación de escritorio te permite generar imágenes, clasificarlas y acceder a tus imágenes almacenadas. Desde el menú principal,elige alguna de las siguientes opciones: \n\n- Seleccionar perfil: permite editar la información del usuario actual  \n\n- Configuración: permite establecer las rutas de los directorios utilizados  \n\n- Etiquetar imágenes: permite agregarle tags a las imágenes de tu directorio de imágenes. Asegúrate de tener un directorio de imágenes seleccionado antes de presionar esta opción \n\n- Generador de memes: permite crear un collage con fotos o imágenes disponibles en nuestra computadora  \n\n- Generador de collage: permite generar un meme a través de combinación de imágenes con texto y emojis \n",  icon=image)


def crear_ventana(usuario):
    '''
    Crea y muestra la ventana de menu principal
    '''
    col = [
        [sg.Button("Etiquetar imágenes", key="-ETIQUETAR-", size=(15,2))],
        [sg.Button("Generar collage", key="-GENERAR COLLAGE-", size=(15,2))],
        [sg.Button("Generar meme", key="-GENERAR MEME-", size=(15,2))],
        [sg.Button("Salir", key="-SALIR-", size=(15,2), button_color="#ff4a3d")]
        ]
    
    layout = [
                [sg.Button("Editar perfil", key="-EDITAR PERFIL-", border_width=0, pad=(20,20)),
                 sg.Push(), sg.Button("Configuracion", key="-CONFIGURACION-", border_width=0, pad=((0,10),(0,0))),
                 sg.Button("Ayuda", key="-AYUDA-", border_width=0, pad=((10,20),(0,0)))],
                [sg.Column(col, key="-COLUMNA BOTONES-", justification="center", pad=(0,30))]
            ]

    window = sg.Window("Menu", layout,finalize=True,size=const.TAM_VENTANAS)
    mostrar_imagenes_botones(window,usuario)
    dir_imagenes, dir_collage, dir_memes = abrir_dirs()

    while True:

        event, values = window.read()

        if event == "-SALIR-":
            window.close()
            inicio.crear_ventana()

        if event == "-EDITAR PERFIL-":
            window.close()
            editar_perfil.crear_ventana(usuario)

        if event == "-CONFIGURACION-":
            window.close()
            configuracion.crear_ventana(usuario)

        if event == "-AYUDA-":
            mostrar_mensaje_ayuda()

        if event == "-GENERAR COLLAGE-":
            if not dir_collage == "":
                window.close()
                dir_collage = os.path.abspath(dir_collage)
                seleccionador_collage.crear_ventana(usuario, dir_collage)
            else:
                sg.Popup("No seleccionaste un directorio de collages")
                window.close()
                configuracion.crear_ventana(usuario)
            
        if event == "-GENERAR MEME-":
            if not dir_memes == "" :
                window.close()
                dir_memes = os.path.abspath(dir_memes)
                seleccionador_memes.crear_ventana(usuario, dir_memes)
            else:
                sg.Popup("No seleccionaste un directorio de memes")
                window.close()
                configuracion.crear_ventana(usuario)
        if event == "-ETIQUETAR-":
            if not dir_imagenes == "" :
                window.close()
                dir_imagenes = os.path.abspath(dir_imagenes)
                etiquetar_imagenes.crear_ventana(usuario,dir_imagenes)
            else:
                sg.Popup("No seleccionaste un directorio de imagenes")
                window.close()
                configuracion.crear_ventana(usuario)

        if event == sg.WIN_CLOSED:
            break

    window.close()
    