import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import json
from pantallas import constantes as const, menu_principal
from . funciones_comunes import actualizar_logs,boton_volver,is_image
import csv
import datetime
import shutil


def convertir_tags(tags):
    '''
    Recibe el string de tags y lo convierte a una lista
    '''
    return tags.split(',')


def obtener_fecha():
    '''
    Devuelve la fecha en formato año/meses/dias/horas/minutos/segundos
    '''
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def checkear_repetidos(window,tag,lista):
    '''
    Se fija si el tag esta repetido, en ese caso no lo agrega a la lista de tags
    '''
    if not (tag in lista):
        lista.append(tag)
        window["-LISTA TAG-"].update(lista)


def obtener_metadatos_imagen(ruta):
    '''
    Recibe una imagen y me devuelve resolucion, tamaño y mimetype
    '''
    imagen = Image.open(ruta)

    # Obtener la resolución de la imagen en formato Ancho x Alto
    resolucion = "{}x{}".format(*imagen.size)
    
    # Obtener el tamaño de la imagen en MB
    tamaño = os.path.getsize(imagen.filename) / (1024 * 1024)
    tamaño = str(round(tamaño,2)) + "MB"
    
    # Obtener el mimetype de la imagen
    mimetype = str(Image.MIME[imagen.format])
    
    return resolucion,tamaño,mimetype


def buscar_imagen(nombre_archivo):
    '''
    Busca una imagen en el archivo CSV por su nombre de archivo
    '''
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos_app", "img_data.csv"), mode='r') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            ruta_rel = fila['ruta relativa']
            # Extrae el nombre de archivo de la ruta relativa
            nombre_archivo_actual = os.path.basename(ruta_rel)
            if nombre_archivo_actual == nombre_archivo:
                return fila
        return None


def guardar_imagen(ruta, nombre, tags, descripcion, ult_perfil,usuario):
    '''
    Guarda los datos de la imagen en el csv
    '''
    ruta_archivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos_app", "img_data.csv")
    # Si la imagen ya se encuentra en el CSV actualizo los tags, la descripcion, ult_perfil y fecha_actualizacion
    with open(ruta_archivo, mode='r', newline='') as archivo:
        lector_csv = csv.DictReader(archivo)
        lista_filas = []
        fila_encontrada = False
        for fila in lector_csv:
            nombre_archivo_actual = os.path.basename(fila['ruta relativa'])
            #Si el archivo se llama igual actualizo sus valores
            if nombre_archivo_actual == nombre:
                fila['tags'] = tags
                fila['texto descriptivo'] = descripcion
                fila['ultimo perfil'] = ult_perfil
                fila['fecha actualizacion'] = obtener_fecha()
                fila_encontrada = True
            lista_filas.append(fila)
    # Si la imagen no se encuentra en el CSV, cargo todos los valores
    if not fila_encontrada:
        # Copio la imagen a la carpeta de imágenes etiquetadas
        shutil.copy2(ruta,os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","imagenes_etiquetadas"))
        # Obtengo los metadatos de la imagen
        tipo, tamaño, resolucion = obtener_metadatos_imagen(ruta)
        fecha_actualizacion = obtener_fecha()
        # Creo un diccionario con los valores de la nueva fila
        nueva_fila = {
            'ruta relativa': nombre,
            'texto descriptivo': descripcion,
            'resolucion': resolucion,
            'tamanio': tamaño,
            'tipo': tipo,
            'tags': tags,
            'ultimo perfil': ult_perfil,
            'fecha actualizacion': fecha_actualizacion
        }
        lista_filas.append(nueva_fila)
    
    # Escribo los cambios en el archivo CSV
    with open(ruta_archivo, mode='w', newline='') as archivo:
        escritor_csv = csv.DictWriter(archivo, fieldnames=lector_csv.fieldnames)
        escritor_csv.writeheader()
        escritor_csv.writerows(lista_filas)

    # Actualizo el archivo de logs
    actualizar_logs("Imagen modificada",usuario) if fila_encontrada else actualizar_logs("Nueva imagen clasificada",usuario)


def actualizar_imagen(window, ruta=None):
    '''
    Actualiza la imagen que aparece en el frame
    '''
    try:
        # En caso de no haber seleccionado ninguna imagen, pone una imagen de placeholder
        if ruta == None:
            ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "image_placeholder.png")
        img = Image.open(ruta)
        img.thumbnail((150, 120))
        img_tk = ImageTk.PhotoImage(img)
        window["-IMAGEN-"].update(data=img_tk)
    except:
        sg.Popup("El archivo seleccionado debe ser una imagen")


def actualizar_informacion_imagen(window,ruta,nombre):
    '''
    Actualiza la información de la imagen en la ventana de la aplicación.
    '''
    fila = buscar_imagen(nombre)
    actualizar_imagen(window,ruta)
    # Si la imagen ya se encuenta en el csv
    if fila is not None:
        # Me guardo los valores que necesito de cada columna
        texto_descriptivo = fila['texto descriptivo']
        resolucion = fila['resolucion']
        tamaño = fila['tamanio']
        tipo = fila['tipo']
        tags = fila['tags']
        lista_tags = convertir_tags(tags)
        # Actualizo los valores en la window
        window["-TITULO IMAGEN-"].update(nombre)
        window["-METADATOS IMAGEN-"].update("|" + tipo + "|" + tamaño + "|" + resolucion + "|")
        window["-DESCRIPCION IMAGEN-"].update(texto_descriptivo)
        window["-LISTA TAG-"].update(lista_tags)
        return lista_tags
    # En el caso de que la imagen no se encuentre en el csv obtengo valores a mostrar
    else:
        tipo,tamaño,resolucion = obtener_metadatos_imagen(ruta)
        window["-TITULO IMAGEN-"].update(nombre)
        window["-METADATOS IMAGEN-"].update("|" + tipo + "|" + tamaño + "|" + resolucion + "|")
        return []
        

def eliminar_tag(window,tag,lista_tags):
    '''
    Elimina el tag de la lista.
    '''
    lista_tags.remove(tag)
    window["-LISTA TAG-"].update(lista_tags)


def reiniciar_lista_tags(window,lista_tags):
    '''
    Limpia la lista de tags.
    '''
    lista_tags.clear()
    window["-LISTA TAG-"].update(lista_tags)


def crear_ventana(usuario,dir_imagenes):
    '''
    Crea y muestra la ventana de etiquetar imágenes.
    '''
    col1 = [
        [sg.LBox([], size=(25, 10), expand_x=True, expand_y=True, key='-LISTA IMAGE-', enable_events=True)],
        [sg.Text("Tag")],
        [sg.Input("Agregar tag", key="-TAG-", size=(25, 1)), sg.Button("Agregar", key="-AGREGAR TAG-")],
        [sg.Text("Texto descriptivo")],
        [sg.Input("Agregar descripción", key="-DESCRIPCION-", size=(35, 1)), sg.Button("Agregar", key="-AGREGAR DESCRIPCION-")]
    ]

    frame = [
        [sg.Text(key="-TITULO IMAGEN-")],
        [sg.Image(key="-IMAGEN-")],
        [sg.Text(key="-METADATOS IMAGEN-")],
        [sg.LBox([],size=(10, 3),expand_x=True,key=("-LISTA TAG-"),enable_events=True,)],
        [sg.Text("Descripción:")],
        [sg.Text(key="-DESCRIPCION IMAGEN-")]
    ]

    layout = [
        [sg.Push(), sg.Button("Volver", key="-VOLVER-",border_width=0)],
        [sg.Column(col1, element_justification='left'),
         sg.Frame(title=None, layout=frame, element_justification='center', expand_x=True, expand_y=True,key="-FRAME-")],
        [sg.Push(), sg.VPush(), sg.Button("Guardar", key="-GUARDAR-", button_color="#65b2db")]
    ]

    window = sg.Window("Etiquetar imagenes", layout, finalize=True, size=const.TAM_VENTANAS)
    actualizar_imagen(window)
    boton_volver(window)
    window["-TITULO IMAGEN-"].update("No hay una imagen seleccionada")

    # Uso list comprehension para mostrar todos los archivos de dir_imagenes
    archivos = [archivo for archivo in os.listdir(dir_imagenes)]
    # Uso filter para remover los subdirectorios de dir_imagenes
    archivos = list(filter(lambda x: is_image(os.path.join(dir_imagenes,x)),archivos))
        
    window['-LISTA IMAGE-'].update(archivos)

    lista_tags = []
    nombre = None
    
    while True:
    
        event, values = window.read()

        if event == "-LISTA IMAGE-":
            # Limpio la descripcion de la imagen
            window["-DESCRIPCION IMAGEN-"].update("")
            reiniciar_lista_tags(window,lista_tags)

            # Me fijo que el directorio tenga algun archivo, para evitar errores al acceder a values
            if values["-LISTA IMAGE-"]:
                nombre = values["-LISTA IMAGE-"][0]
                ruta = os.path.join(dir_imagenes,nombre)
                lista_tags = actualizar_informacion_imagen(window,ruta,nombre)
                
        if event == "-AGREGAR TAG-":
            checkear_repetidos(window,values["-TAG-"],lista_tags)

        if event == "-AGREGAR DESCRIPCION-":
            window["-DESCRIPCION IMAGEN-"].update(values["-DESCRIPCION-"])

        if event == "-LISTA TAG-":
            if lista_tags:
                eliminar_tag(window,values["-LISTA TAG-"][0],lista_tags)

        if event == "-VOLVER-":
            window.close()
            menu_principal.crear_ventana(usuario)

        if event == "-GUARDAR-":
            # Solo guardo si clickee alguna imagen del directorio
            if nombre is not None:
                ruta = os.path.join(dir_imagenes,nombre)
                # Agarro el texto de la descripcion
                descripcion = window["-DESCRIPCION IMAGEN-"].get()
                perfil = usuario["Nick"]
                # Convertir tags en string
                tags = ",".join(lista_tags)
                guardar_imagen(ruta,nombre,tags,descripcion,perfil,usuario)

        if event == sg.WIN_CLOSED:
            break

    window.close()