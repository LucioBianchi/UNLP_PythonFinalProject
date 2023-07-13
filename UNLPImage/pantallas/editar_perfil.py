import shutil
import PySimpleGUI as sg
from pantallas import menu_principal
from pantallas import constantes as const
import os
import os.path
import json
from PIL import Image, ImageTk
from . funciones_comunes import boton_volver, actualizar_logs


def checkear_valores(values):
    '''
    Comprueba si los valores ingresados por el usuario son validos. Si hay errores, muestra una ventana emergente
    con los mensajes de error.
    '''
    errores = []
    if not values["-NOMBRE-"].strip().isalpha():
        errores.append("Debe ingresar caracteres alfabeticos en el nombre")
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


def buscar_usuario(perfiles, nick):
    '''
    Busca la posicion en la que se encuentra el usuario que se le pasa por parametro y la devuelve.
    '''
    for i, perfil in enumerate(perfiles["datos"]):
        if perfil["Nick"] == nick:
            return i
    return None


def actualizar_imagen(element,ruta=""):
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


def guardar_usuario(values, usuario):
    '''
    Cambia los valores en el json del usuario a editar.
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","perfiles.json"),"r+") as archivo:
        perfiles = json.load(archivo)
        # En caso de que no se seleccione una imagen, se queda con la que tenia
        if values["-AVATAR SELECCIONADO-"] == "":
            img_path = usuario["Avatar"]
        else:
            img_path = values["-AVATAR SELECCIONADO-"]
        dir_path = os.path.join("UNLPImage","datos_app","avatares")
        rel_path = os.path.join("UNLPImage","datos_app","avatares",os.path.basename(img_path))
        # Si la imagen ya existe en el directorio de avatares, no la copia
        if not os.path.exists(rel_path):
            # shutil.copy2 agarra el archivo del path y lo copia en el directorio especificado
            shutil.copy2(img_path, os.path.join(dir_path))
        #En linux cambio la barra simple por doble barra para tener un path universal
        rel_path.replace("/","\\")
        #Guardo los valores ya editados en la ventana
        nuevos_valores = {"Nick":usuario["Nick"],
                          "Nombre": values["-NOMBRE-"],
                          "Edad": values["-EDAD-"],
                          "Genero": values["-GENERO-"],
                          "Avatar": rel_path}
        #Busco la posicion del usuario a editar en el json
        pos_usuario_editar = buscar_usuario(perfiles, usuario["Nick"])
        perfiles["datos"][pos_usuario_editar].update(nuevos_valores) # guardo la pos del usuario dentro del diccionario
        archivo.seek(0)
        #Trunco el archivo para remover la informacion extra 
        archivo.truncate()
        json.dump(perfiles,archivo,ensure_ascii=False,indent=4)
    return nuevos_valores


def crear_ventana(usuario):
    '''
    Crea y muestra la ventana de editar perfil.
    '''
    col1 = [
        [sg.Text("Nombre")],
        [sg.Input(default_text=usuario["Nombre"],key="-NOMBRE-")],
        [sg.Text("Edad")],
        [sg.Input(default_text=usuario["Edad"],key="-EDAD-")],
        [sg.Text("Género autopercibido")],
        [sg.Combo(values=["Masculino","Femenino","Otro"],default_value=usuario["Genero"], enable_events=True, size=(43,1), key= "-GENERO-")],
        [sg.Button("Guardar", key="-GUARDAR-", button_color="#65b2db", pad=(0,20))]
    ]

    texto_nick = [
        [sg.Text("Nick:", font=(18)), 
        sg.Text(usuario["Nick"], font=(18), text_color="#65b2db")]
    ]

    col2 = [
        [sg.Frame(title=None,layout=texto_nick, pad=(0,5))],
        [sg.Image(key="-IMAGE-")],
        [sg.FileBrowse(key="-AVATAR SELECCIONADO-", enable_events=True, pad=(0,5))],
    ]

    layout = [
        [sg.Push(), sg.Button("Volver", key="-VOLVER-",border_width=0)],
        [sg.Column(col1, element_justification='center', justification="center", pad=(10, 40)),
         sg.Column(col2, element_justification='center', justification="center", pad=(20, 40))]
    ]

    window = sg.Window("Editar perfil", layout, finalize=True, size= const.TAM_VENTANAS)
    actualizar_imagen(window["-IMAGE-"], usuario["Avatar"])
    boton_volver(window)
    
    while True:

        event, values = window.read()

        if event == "-GUARDAR-":
            if checkear_valores(values):
                usuario = guardar_usuario(values, usuario)
                actualizar_logs("modificar_perfil",usuario)

        if event == "-VOLVER-":
            window.close()
            menu_principal.crear_ventana(usuario)

        if event == "-AVATAR SELECCIONADO-":
            ruta = values["-AVATAR SELECCIONADO-"]
            actualizar_imagen(window["-IMAGE-"],ruta)
            
        if event == sg.WIN_CLOSED:
            break

    window.close()