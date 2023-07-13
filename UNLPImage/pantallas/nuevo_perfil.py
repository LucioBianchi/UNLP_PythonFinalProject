import PySimpleGUI as sg
from pantallas import inicio, menu_principal
from pantallas import constantes as const
import os.path
import json
import shutil
from PIL import Image, ImageTk
from . funciones_comunes import boton_volver, actualizar_logs 


def checkear_valores(values):
    '''
    Comprueba si los valores ingresados por el usuario son validos. Si hay errores, muestra una ventana
    emergente con los mensajes de error.
    '''
    errores = []
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","perfiles.json")) as archivo:
        datos = json.load(archivo)
        if any(val["Nick"] == values["-NICK-"] for val in datos["datos"]):
            errores.append("El Nick ingresado ya existe")
    if not values["-NICK-"].strip().isalnum():
        errores.append("El nick solo acepta caracteres alfabéticos y números")
    if not values["-NOMBRE-"].strip().isalpha():
        errores.append("El nombre solo acepta caracteres alfabéticos")
    if not values["-EDAD-"].isdigit():
        errores.append("La edad debe ser un número entero")
    if values["-GENERO-"] not in ["Masculino", "Femenino", "Otro"]:
        errores.append("El género seleccionado no es válido")

    if errores:
        mensaje_error = "\n".join(errores)
        sg.popup_error(mensaje_error)
        return False
    else:
        return True


def guardar_usuario(values):
    '''
    Guardo el usuario en el json.
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","perfiles.json"),"r+") as archivo:
        nuevos_datos = json.load(archivo)
        # En caso de que no se seleccione una imagen, guardamos el placeholder
        if values["-AVATAR SELECCIONADO-"] == '':
            rel_path = os.path.join("UNLPImage","assets","profile_placeholder.png")
        else:
            img_path = values["-AVATAR SELECCIONADO-"]
            dir_path = os.path.join("UNLPImage","datos_app","avatares")
            rel_path = os.path.join(dir_path,os.path.basename(img_path))
            # Si la imagen ya existe en el directorio de avatares, no la copia
            if not os.path.exists(rel_path):
                # shutil.copy2 agarra el archivo del path y lo copia en el directorio especificado
                shutil.copy2(img_path, os.path.join(dir_path))
            # En linux cambio la barra simple por doble barra para tener un path universal
            rel_path.replace(os.path.sep,"\\")

        valores = {"Nick": values["-NICK-"],
                   "Nombre": values["-NOMBRE-"],
                   "Edad": values["-EDAD-"],
                   "Genero": values["-GENERO-"],
                   "Avatar": rel_path}
        # Le agrego a la lista de usuarios del json el nuevo usuario
        nuevos_datos["datos"].append(valores)
        archivo.seek(0)
        json.dump(nuevos_datos,archivo,ensure_ascii=False,indent=4)
    return valores


def actualizar_imagen(element,ruta):
    '''
    Actualiza la imagen si es valida, sino muestra una ventana de error.
    '''
    try:
        image = Image.open(ruta)
        image.thumbnail((140,140))
        image_tk = ImageTk.PhotoImage(image)
        element.update(data=image_tk)
    except:
        sg.popup_error("Hubo un error con el archivo seleccionado, se debe seleccionar una imagen")


def crear_ventana():
    '''
    Crea y muestra la ventana de nuevo perfil.
    '''
    col1 = [
        [sg.Text("Nick o alias")],
        [sg.Input(key="-NICK-")],
        [sg.Text("Nombre")],
        [sg.Input(key="-NOMBRE-")],
        [sg.Text("Edad")],
        [sg.Input(key="-EDAD-")],
        [sg.Text("Género autopercibido")],
        [sg.Combo(values=["Masculino","Femenino","Otro"], enable_events=True, size=(43,1), key= "-GENERO-")],
        [sg.Button("Guardar", key="-GUARDAR-", button_color="#65b2db",pad=(0,20))],
    ]

    col2 = [
        [sg.Image(key="-IMAGE-")],
        [sg.FileBrowse(key="-AVATAR SELECCIONADO-", enable_events=True, pad=(0,3))],
    ]

    layout = [
        [sg.Push(), sg.Button("Volver", key="-VOLVER-", border_width=0)],
        [sg.Column(col1, element_justification='center', justification="center", pad=(10, 40)),
         sg.Column(col2, element_justification='center', justification="center", pad=(20, 40))],
    ]

    window = sg.Window("Agregar perfil", layout, finalize=True, size=const.TAM_VENTANAS)
    img_por_defecto = os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","profile_placeholder.png")
    actualizar_imagen(window["-IMAGE-"],img_por_defecto)
    boton_volver(window)
    

    while True:

        event, values = window.read()

        if event == "-GUARDAR-":
            if checkear_valores(values):
                window.close()
                usuario = guardar_usuario(values)
                actualizar_logs("nuevo perfil",usuario)
                menu_principal.crear_ventana(usuario)

        if event == "-VOLVER-":
            window.close()
            inicio.crear_ventana()

        if event == "-AVATAR SELECCIONADO-":
            ruta = values["-AVATAR SELECCIONADO-"]
            actualizar_imagen(window["-IMAGE-"],ruta)

        if event == sg.WIN_CLOSED:
            break

    window.close()