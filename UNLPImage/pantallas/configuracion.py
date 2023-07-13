import PySimpleGUI as sg
from pantallas import constantes as const, menu_principal
from datos_app.dir import dirs
import json
import os
from . funciones_comunes import actualizar_logs, boton_volver


def checkear_valores(values):
    '''
    Comprueba si los directorios seleccionados por el usuario existen y actualiza los directorios de la clase
    Dirs en caso de que existan. Si hay errores, muestra una ventana emergente con los mensajes de error.
    '''
    errores = []
    if(values["-IMG DIR-"]):
        if(os.path.isdir(values["-IMG DIR-"])):
            dirs.set_dir_imagenes(os.path.relpath(values["-IMG DIR-"]))
        else:
            errores.append("El directorio de imagenes seleccionado no existe")
    if(values["-COLL DIR-"]):
        if(os.path.isdir(values["-COLL DIR-"])):
            dirs.set_dir_collage(os.path.relpath(values["-COLL DIR-"]))
        else:
            errores.append("El directorio de collage seleccionado no existe")
    if(values["-MEME DIR-"]):
        if(os.path.isdir(values["-MEME DIR-"])):
            dirs.set_dir_memes(os.path.relpath(values["-MEME DIR-"]))
        else:
            errores.append("El directorio de memes seleccionado no existe")
    if errores:
        mensaje_error = "\n".join(errores)
        sg.popup_error(mensaje_error)


def guardar_dir():
    '''
    Guarda los directorios seleccionados por el usuario en un archivo JSON.
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","dirs.json"), "w") as directorios:
        json.dump({
            "Dir Imagenes": dirs.get_dir_imagenes(), 
            "Dir Collage": dirs.get_dir_collage(), 
            "Dir Memes": dirs.get_dir_memes()
            },directorios)


def cargar_dirs(window):
    '''
    Carga los directorios guardados en el archivo JSON y los muestra en la ventana.
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","dirs.json"), "r") as dirs:
        data = json.load(dirs)
        window["-IMG DIR-"].update(data["Dir Imagenes"])
        window["-COLL DIR-"].update(data["Dir Collage"])
        window["-MEME DIR-"].update(data["Dir Memes"])


def crear_ventana(usuario):
    '''
    Crea y muestra la ventana de configuración
    '''
    # Creo el path al que te lleva el browse de directorio de imagenes ( Directorio de imagenes de prueba )
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","imagenes_prueba")

    columna = [
        [sg.Text("Directorio de imagenes")],
        [sg.Input(key="-IMG DIR-"),sg.FolderBrowse(key="-BROWSE IMG-", initial_folder=path, enable_events=True)],
        [sg.Text("Directorio de collages")],
        [sg.Input(key="-COLL DIR-"),sg.FolderBrowse(key="-BROWSE COLL-", enable_events=True)],
        [sg.Text("Directorio de memes")],
        [sg.Input(key="-MEME DIR-"),sg.FolderBrowse(key="-BROWSE MEME-", enable_events=True)],
        [sg.Button("Guardar", key="-GUARDAR-", button_color="#65b2db", pad=(150,35))]
    ]

    layout = [
        [sg.Push(),sg.Button("Volver", key="-VOLVER-",border_width=0)],
        [sg.Column(columna, justification="center", pad=(0,40))],
        ]

    window = sg.Window("Configuracion", layout,finalize=True,size=const.TAM_VENTANAS)
    cargar_dirs(window)
    boton_volver(window)

    while True:

        event, values = window.read()

        if event == "-VOLVER-":
            window.close()
            menu_principal.crear_ventana(usuario)

        if event == "-GUARDAR-":
            checkear_valores(values)
            guardar_dir()
            actualizar_logs("Configuracion modificada",usuario)

        if event == sg.WIN_CLOSED:
            break

    window.close()