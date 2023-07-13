import PySimpleGUI as sg
from pantallas import constantes as const, menu_principal, generador_memes
from . funciones_comunes import boton_volver
import os
import json
from PIL import Image, ImageTk

def cargar_templates():
    '''
    Cargo los datos del JSON de templates en la variable datos
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","templates_memes.json"),"r") as archivo:
        datos = json.load(archivo)
    return datos


def buscar_template(nombre,datos):
    '''
    Recibe un nombre y devuelve un template
    '''
    return [elem for elem in datos["datos"] if elem["nombre"] == nombre][0]


def actualizar_imagen(element,ruta=None):
    '''
    Actualiza la imagen.
    '''
    if ruta == None:
       ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "meme_placeholder.jpg")
    else: ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","templates_meme",ruta)
    image = Image.open(ruta)
    image.thumbnail((250,250), Image.ANTIALIAS)
    image_tk = ImageTk.PhotoImage(image)
    element.update(data=image_tk)


def crear_ventana(usuario,dir_memes):
    '''
    Crea y muestra la ventana de seleccionador de memes
    '''
    datos = cargar_templates()
    templates = [template["nombre"] for template in datos["datos"]]

    col1 = [
            [sg.Text("Seleccionar template")],
            [sg.LBox(values=templates,size=(30, 6),
                     expand_x=True,
                     key=("-LISTA TEMPLATE-"),
                     enable_events=True,)],
            ]
    
    col2 = [
            [sg.Text("Previsualizacion", justification="left" )],
            [sg.Image(key="-IMAGE-")]
            ]

    layout = [
                [sg.Push(), sg.Button("Volver", key="-VOLVER-", border_width=0)],
                [sg.Column(col1, expand_y=True),
                 sg.Push(), 
                 sg.Column(col2, expand_y=True, expand_x=True, pad=((30,0),0))],
                [sg.Push(),
                 sg.Button("Generar", key="-GENERAR-", button_color="#65b2db",pad=((0,17),(5,10)))],    
            ]

    window = sg.Window("Generador memes", layout,finalize=True,size=const.TAM_VENTANAS)
    boton_volver(window)
    actualizar_imagen(window["-IMAGE-"])
    template = None

    while True:
        
        event, values = window.read()
        
        if event == "-VOLVER-":
            window.close()
            menu_principal.crear_ventana(usuario)
        
        if event == "-LISTA TEMPLATE-":
            template = buscar_template(values["-LISTA TEMPLATE-"][0],datos)
            actualizar_imagen(window["-IMAGE-"],template["image"])
        
        if event == "-GENERAR-":
            if template != None:
                window.close()
                generador_memes.crear_ventana(usuario, template,dir_memes)
            else:
                sg.Popup("Debe seleccionar un template")
        
        if event == sg.WIN_CLOSED:
            break

    window.close()