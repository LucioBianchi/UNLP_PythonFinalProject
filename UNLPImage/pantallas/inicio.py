import PySimpleGUI as sg
from pantallas import nuevo_perfil, menu_principal
from pantallas import constantes as const
from . funciones_comunes import imagen_boton, normalizar_path
import os
import json


def cargar_usuarios():
    '''
    Cargo los datos del JSON de perfiles en la variable datos
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","perfiles.json"),"r") as archivo:
        datos = json.load(archivo)
    return datos


def inicializar_perfiles(datos):
    '''
    Crea los botones necesarios para mostrar los perfiles del JSON. Devuelve la lista de botones
    y una lista de indices que indican qué perfiles estoy mostrando en los botones
    '''
    cant_perfiles = len(datos["datos"]) if len(datos["datos"]) < const.MAX_PERFILES else const.MAX_PERFILES
    # Me guardo un indice para recorrer la lista de perfiles mostrados
    indice_actuales = [0, cant_perfiles-1]
    # Guardo en la lista tantos botones como perfiles necesite mostrar
    lista = [sg.Button(datos["datos"][i]["Nick"], key=f"-BOTON-PERFIL{i}-", border_width=0) for i in range(cant_perfiles)]
    return lista, indice_actuales


def mostrar_perfiles(window, indices_actuales,datos):
    '''
    Hace un update en los botones de los perfiles para mostrar al perfil correcto con su imagen correspondiente
    '''
    # Toma como indice los valores que se encuentran entre los indices_actuales
    for i in range(indices_actuales[0],indices_actuales[1]+1):
        image = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), normalizar_path(datos["datos"][i]["Avatar"]))
        image_64 = imagen_boton(image,resize=const.TAM_PERFILES,round=True)
        # Hago un update de la imagen y del nombre del usuario
        window[f"-BOTON-PERFIL{i % const.MAX_PERFILES}-"].update(
            datos["datos"][i]["Nick"],
            image_data=image_64, 
            button_color=sg.theme_background_color(), visible=True)


def mostrar_imagenes_botones(window):
    '''
    Actualiza las imagenes de varios botones
    '''
    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "addsymbol.png")
    image_64 = imagen_boton(image,resize=const.TAM_PERFILES)
    window["-AGREGAR PERFIL-"].update(image_data=image_64)

    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "left_arrow.png")
    image_64 = imagen_boton(image,resize=(40,40))
    window["-VER MENOS-"].update(image_data=image_64, button_color=sg.theme_background_color())

    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "right_arrow.png")
    image_64 = imagen_boton(image,resize=(40,40))
    window["-VER MAS-"].update(image_data=image_64, button_color=sg.theme_background_color())


def boton_ver_mas(indices_actuales,datos):
    '''
    Actualiza la lista de indices_actuales cuando se presiona el boton "ver mas". Devuelve
    True or False dependiendo de si se pudo llevar a cabo o no la operación
    '''
    cant_perfiles = len(datos["datos"])
    if cant_perfiles-1 > indices_actuales[1]:
        indices_actuales[0] = indices_actuales[0] + const.MAX_PERFILES
        indices_actuales[1] = indices_actuales[1] + const.MAX_PERFILES
        if indices_actuales[1] > cant_perfiles-1:
            indices_actuales[1] = cant_perfiles-1
        return True
    else:
        return False
    

def boton_ver_menos(indices_actuales,datos):
    '''
    Actualiza la lista de indices_actuales cuando se presiona el boton "ver menos". Devuelve
    True or False dependiendo de si se pudo llevar a cabo o no la operación
    '''
    if indices_actuales[0] > const.MAX_PERFILES-1:
        indices_actuales[1] = indices_actuales[0] - 1
        indices_actuales[0] = indices_actuales[0] - const.MAX_PERFILES
        return True
    else:
        return False


def ocultar_agregar_perfil(window):
    '''
    Oculta momentaneamente el boton de agregar perfil pare evitar errores al mostrar perfiles
    '''
    window["-AGREGAR PERFIL-"].update(visible=False)
    window["-AGREGAR PERFIL-"].update(visible=True)


def ocultar_botones(window,indices_actuales):
    '''
    Oculta los botones de los perfiles que no deberian mostrarse cuando la cantidad de perfiles 
    a mostrar es menor a MAX_PERFILES
    '''
    cant_ocultar =  const.MAX_PERFILES - (indices_actuales[1] - indices_actuales[0])
    for i in range(const.MAX_PERFILES - cant_ocultar + 1, const.MAX_PERFILES):
        window[f"-BOTON-PERFIL{i}-"].update(visible=False)


def buscar_usuario(nombre_buscado,datos):
    '''
    Permite buscar un nick del usuario deseado por parametro en la lista de perfiles
    '''
    # Uso list comprehension para devolver el usuario buscado
    return [elem for elem in datos["datos"] if elem["Nick"] == nombre_buscado][0]


def crear_ventana():
    '''
    Crea y muestra la ventana de inicio
    '''
    datos = cargar_usuarios()
    botones, indices_actuales = inicializar_perfiles(datos)

    col1 = [
                  botones,
    ]

    col2 = [
                [sg.Button("VER MÁS", key="-VER MENOS-", pad=((10,0),(20,0)), border_width=0),
                sg.Button("VER MENOS", key="-VER MAS-", pad=((10,0),(20,0)),border_width=0)]
    ]

    elem = [
        [sg.Column(col1,justification="center"),
        sg.Button("Agregar perfil", key="-AGREGAR PERFIL-",button_color=sg.theme_background_color(), border_width=0)],
        [sg.Column(col2,justification="center")]
    ]

    col_principal = [
        [sg.Image(key="-IMAGEN-")],
        [sg.Frame(title=None,layout=elem,border_width=0)]
    ]

    layout = [
        [sg.Column(col_principal,justification="center",pad=(0,60))]
    ]


    window = sg.Window("Inicio", layout, finalize=True, size=const.TAM_VENTANAS)
    mostrar_perfiles(window,indices_actuales,datos)
    mostrar_imagenes_botones(window)

    while True:
        
        event, values = window.read()

        if event and event.split("-")[1] == "BOTON":
            window.close()
            usuario = buscar_usuario(window[event].get_text(),datos)
            usuario["Avatar"] = normalizar_path(usuario["Avatar"])
            menu_principal.crear_ventana(usuario)
        
        if event == "-VER MAS-":
            if(boton_ver_mas(indices_actuales,datos)):
                ocultar_botones(window,indices_actuales)
                mostrar_perfiles(window,indices_actuales,datos)

        if event == "-VER MENOS-":
            if(boton_ver_menos(indices_actuales,datos)):
                mostrar_perfiles(window,indices_actuales,datos)
                ocultar_agregar_perfil(window)

        if event == "-AGREGAR PERFIL-":
            window.close()
            nuevo_perfil.crear_ventana()
        
        if event == sg.WIN_CLOSED:
            break
            
    window.close()
    

