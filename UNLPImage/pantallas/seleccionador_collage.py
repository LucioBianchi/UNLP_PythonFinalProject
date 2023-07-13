import PySimpleGUI as sg
from pantallas import generador_collage
from pantallas import constantes as const, menu_principal
from . funciones_comunes import boton_volver,imagen_boton
import os
import json


def cargar_diseños():
    '''
    Cargo los datos del JSON de diseños en la variable datos
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","diseños_collage.json"),"r") as archivo:
        datos = json.load(archivo)
    return datos["datos"]


def cargar_templates(datos,window):
    '''
    Les asigna la imagen correspondiente a los templates del JSON
    '''
    indice = 0
    for template in datos:
        indice += 1
        if indice > len(datos):
            break
        image = os.path.join("UNLPImage","assets","diseños_collage",template["image"])
        image64 = imagen_boton(image,resize=(105,135))
        window[f"-TEMPLATE-{indice}-"].update(
            text=datos[indice-1]["image"],
            image_data=image64,
            button_color=sg.theme_background_color(),
        )


def buscar_template(template_buscado,datos):
    '''
    Permite buscar un template pasado por parametro en el json de diseños
    '''
    # Uso list comprehension para devolver el template buscado
    return [elem for elem in datos if elem["image"] == template_buscado][0]


def crear_ventana(usuario, dir_collage):
    '''
    Crea y muestra la ventana de seleccionador collage
    '''
    col = [
        [sg.Button(key="-TEMPLATE-1-", border_width=0),
                sg.Button(key="-TEMPLATE-2-", border_width=0),
                sg.Button(key="-TEMPLATE-3-", border_width=0),],
        [sg.Button(key="-TEMPLATE-4-", border_width=0),
                sg.Button(key="-TEMPLATE-5-", border_width=0),
                sg.Button(key="-TEMPLATE-6-", border_width=0),]
        ]

    layout = [
                [sg.Text("Selecciona un diseño",justification="center",font=('Work Sans', 16),pad=((210,0),0)),
                sg.Push(), sg.Button("Volver", key="-VOLVER-",border_width=0)],
                [sg.Column(col, key="-COLUMNA BOTONES-", justification="center")]
            ]

    window = sg.Window("Seleccionador collage", layout,finalize=True,size=const.TAM_VENTANAS)
    boton_volver(window)
    datos = cargar_diseños()
    cargar_templates(datos,window)
    
    while True:

        event, values = window.read()

        if event and event.split("-")[1] == "TEMPLATE":
            window.close()
            collage_seleccionado = buscar_template(window[event].get_text(),datos)
            generador_collage.crear_ventana(usuario, collage_seleccionado, dir_collage)

        if event == "-VOLVER-":
            window.close()
            menu_principal.crear_ventana(usuario)
            
        if event == sg.WIN_CLOSED:
            break

    window.close()