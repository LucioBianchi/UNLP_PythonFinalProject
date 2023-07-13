import PySimpleGUI as sg
from pantallas import constantes as const, seleccionador_collage
from . funciones_comunes import boton_volver,is_image, imagen_boton, actualizar_logs
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


def imagenes_seleccionadas(values,collage,errores):
    '''
    Chequea que se hayan seleccionado todas las imágenes
    '''
    for i in range(len(collage["image_boxes"])):
        if values[f"-IMAGEN-{i + 1}-"] == "":
            errores.append(f"Se debe seleccionar la imágen {i + 1}")
    
def titulo_valido(titulo,values,collage):
    '''
    Chequea que un título tengo menos de 20 caracteres y se hayan seleccionado todas las imágenes
    '''
    errores = []
    if len(titulo) >= 20:
        errores.append("El título debe tener menos de 20 caracteres")
    
    imagenes_seleccionadas(values,collage,errores)

    if errores:
        mensaje_error = "\n".join(errores)
        sg.popup_error(mensaje_error)
        return False
    else:
        return True
    
def guardar_valido(titulo,values,collage):
    '''
    Checkea que se haya seleccionado un título y se hayan seleccionada todas las imágenes. 
    Sino, muestra una ventana emergente con los mensajes de error.
    '''
    errores = []
    if titulo == "":
        errores.append("Se le debe asignar un título al collage")
    
    imagenes_seleccionadas(values,collage,errores)

    if errores:
        mensaje_error = "\n".join(errores)
        sg.popup_error(mensaje_error)
        return False
    else:
        return True

def es_valida(image_path):
    '''
    Chequea que el archivo seleccionado sea una imágen y que esté etiquetada
    '''
    nombre_archivo = os.path.basename(image_path)
    ruta_archivo = os.path.join("UNLPImage", "datos_app", "imagenes_etiquetadas", nombre_archivo)
    if is_image(image_path):
        if os.path.isfile(ruta_archivo):
            return True
        else: sg.popup("La imágen debe estar previamente etiquetada")
    else: sg.popup("Debe seleccionar una imagen")
    return False


def actualizar_botones(window,collage):
    '''
    Actualiza la visibilidad de los botones dependiendo del collage seleccionado
    '''
    for i in range(len(collage["image_boxes"])):
        window[f"-IMAGEN-{i + 1}-"].update(visible=True)


def inicializar_diseño(window,collage):
    '''
    Muestra en pantalla el diseño que se seleccionó
    '''
    # Utilizo un formato para utilizar otros assets
    filename, extension = os.path.splitext(collage["image"])
    template_con_numeros = f"{filename}(2){extension}"
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","diseños_collage",template_con_numeros)
    image = Image.open(ruta)
    image.thumbnail(const.TAN_IMG)
    image_tk = ImageTk.PhotoImage(image)
    window["-IMAGE-"].update(data=image_tk)


def agregar_titulo(window, image_original, text, modify_original=True):
    '''
    Le agrega un título a la imágen
    '''
    # Formateo para que el título quede más prolijo
    text = f"  {text}  "

    # No escribo sobre la imagen original a no ser que sea la que tengo que guardar
    if modify_original:
        image_to_modify = image_original
    else:
        image_to_modify = image_original.copy()

    draw = ImageDraw.Draw(image_to_modify)

    # Define al fuente y el tamaño
    font = ImageFont.truetype("arial.ttf", 20)

    # Define el color del texto y el del fondo
    text_color = (0, 0, 0)  # Negro
    background_color = (255, 255, 255)  # Blanco

    # Obtiene el tamaño del texto
    text_width, text_height = draw.textsize(text, font=font)

    # Calcula la posición del texto en la esquina inferior izquierda
    text_position = (0, image_to_modify.height - text_height)

    # Crea un rectángulo con el tamaño del texto
    background_rectangle = [
        text_position[0],
        text_position[1],
        text_position[0] + text_width,
        text_position[1] + text_height,
    ]

    # Dibuja el rectangulo con el color de fondo
    draw.rectangle(background_rectangle, fill=background_color)

    # Dibuja el texto por encima del rectangulo
    draw.text(text_position, text, fill=text_color, font=font)

    img_mostrar = image_to_modify.copy()
    img_mostrar.thumbnail(const.TAN_IMG)

    image_tk = ImageTk.PhotoImage(img_mostrar)
    window["-IMAGE-"].update(data=image_tk)

    if modify_original:
        return image_to_modify
    else:
        return image_original


def agregar_imagen_en_coordenadas(window, img_original, imagen_nueva, collage, nro_imagen):
    '''
    Agrega la imagen seleccionada en el lugar que corresponde
    '''
    # Abre las imágenes usando Pillow
    img_nueva = Image.open(imagen_nueva)
    coordenadas = collage["image_boxes"][nro_imagen-1]

    # Calcula las coordenadas de la imagen nueva en base al tamaño de la imagen original
    x1 = coordenadas["top_left_x"]
    y1 = coordenadas["top_left_y"]
    x2 = coordenadas["bottom_right_x"]
    y2 = coordenadas["bottom_right_y"]
    
    # Calcula el ancho y alto de la región donde se pegará la imagen nueva
    ancho = x2 - x1
    alto = y2 - y1
    
    # Redimensiona la imagen nueva para ajustarla dentro de las coordenadas
    img_nueva_redimensionada = img_nueva.resize((ancho, alto))
    
    # Pega la imagen nueva redimensionada en la imagen original en las coordenadas especificadas
    img_original.paste(img_nueva_redimensionada, (x1, y1))

    img_mostrar = img_original.copy()
    img_mostrar.thumbnail(const.TAN_IMG)

    image_tk = ImageTk.PhotoImage(img_mostrar)
    window["-IMAGE-"].update(data=image_tk)
    
    return img_original


def guardar_imagen(image,titulo,dir_collage):
    '''
    Guarda la imagen con el título como nombre de archivo
    '''
    path = os.path.join(dir_collage,  f"{titulo}.png")
    if not os.path.isfile(path):
        image.save(path)
    else: sg.popup("Ya existe un archivo con ese título en el directorio de collage")

def generar_texto_valores(values,collage):
    '''
    Genera los valores que se devuelven en el logs
    '''
    aux_text = ""
    for i in range(len(collage["image_boxes"])):
        ruta_archivo = values[f"-IMAGEN-{i + 1}-"]
        nombre_archivo = os.path.basename(ruta_archivo)
        aux_text += nombre_archivo + ";"
    return aux_text[:-1]


def crear_ventana(usuario, collage, dir_collage):
    '''
    Crea y muestra la ventana de generador collage
    '''
    col1 = [
        [sg.FileBrowse("Seleccionar imágen 1", key="-IMAGEN-1-", 
                        enable_events=True, visible=False, pad=(5,(10,20)))],
        [sg.FileBrowse("Seleccionar imágen 2", key="-IMAGEN-2-", 
                        enable_events=True, visible=False, pad=(5,(0,20)))],
        [sg.FileBrowse("Seleccionar imágen 3", key="-IMAGEN-3-", 
                        enable_events=True, visible=False, pad=(5,(0,20)))],
        [sg.FileBrowse("Seleccionar imágen 4", key="-IMAGEN-4-",
                        enable_events=True, visible=False, pad=(5,(0,20)))],
        [sg.Text("Título:",  key="-TITULO-", pad=(5,(0,5)))],
        [sg.Input(key="-TITULO-INPUT-", size=30 ),
         sg.Button("Agregar",key="-CAMBIAR-TITULO-", border_width=0)]
    ]
    
    col2 = [
        [ sg.Image(key="-IMAGE-", expand_x=True)]
    ]

    layout = [
                [sg.Push(), sg.Button("Volver", key="-VOLVER-", border_width=0)],
                [sg.Column(col1, expand_y=True, element_justification="left",pad=((20,42),0)),
                 sg.Push(),sg.Column(col2, expand_y=True)],
                [sg.Push(), sg.Button("Guardar", key="-GUARDAR-", button_color="#65b2db",pad=(15,(10,20)))]
            ]

    window = sg.Window("Generador collage", layout,finalize=True,size=const.TAM_VENTANAS)
    boton_volver(window)
    inicializar_diseño(window,collage)
    actualizar_botones(window,collage)

    image = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon_ok.png")
    image_64 = imagen_boton(image,resize=(25,25))
    window["-CAMBIAR-TITULO-"].update(image_data=image_64, button_color=sg.theme_background_color())
    # Utilizo un formato para utilizar otros assets
    filename, extension = os.path.splitext(collage["image"])
    template_con_numeros = f"{filename}(2){extension}"
    ruta_original = os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","diseños_collage",template_con_numeros)
    img_original = Image.open(ruta_original)
    titulo = ""

    while True:

        event, values = window.read()

        if event and event.split("-")[1] == "IMAGEN":
            nro_imagen = int(event.split("-")[2])
            img_nueva = values[event]
            if es_valida(img_nueva):
                img_original = agregar_imagen_en_coordenadas(window,img_original,img_nueva,collage,nro_imagen)

        if event == "-CAMBIAR-TITULO-":
            titulo = values["-TITULO-INPUT-"]
            if titulo_valido(titulo,values,collage):
                img_original = agregar_titulo(window,img_original,titulo,False)
                
        if event == "-GUARDAR-":
            if guardar_valido(titulo,values,collage):
                img_original = agregar_titulo(window,img_original,titulo)
                guardar_imagen(img_original, titulo, dir_collage)
                log_valores = generar_texto_valores(values,collage)
                actualizar_logs("nuevo_collage",usuario,log_valores,titulo)

        if event == "-VOLVER-":
            window.close()
            seleccionador_collage.crear_ventana(usuario, dir_collage)
            
        if event == sg.WIN_CLOSED:
            break

    window.close()